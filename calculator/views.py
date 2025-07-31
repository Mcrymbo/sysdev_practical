from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import VCFTable, OilTonnage
from .forms import OilTonnageForm
import math

def round_to_nearest(value, step):
    """Round a value to the nearest step"""
    return round(value / step) * step

def get_vcf(density, temperature):
    """
    Get VCF value from VCFTable based on rounded density and temperature
    """
    # Round density to nearest 0.5
    rounded_density = round_to_nearest(density, 0.5)
    # Round temperature to nearest 0.25
    rounded_temperature = round_to_nearest(temperature, 0.25)
    
    try:
        vcf_entry = VCFTable.objects.get(
            density=rounded_density,
            temperature=rounded_temperature
        )
        return vcf_entry.vcf
    except VCFTable.DoesNotExist:
        # If no exact match, try to find the closest match
        # This is a fallback - in production you'd want more sophisticated interpolation
        closest_vcf = VCFTable.objects.filter(
            density__lte=rounded_density + 0.5,
            density__gte=rounded_density - 0.5,
            temperature__lte=rounded_temperature + 0.25,
            temperature__gte=rounded_temperature - 0.25
        ).first()
        
        if closest_vcf:
            return closest_vcf.vcf
        else:
            # Default VCF if no match found
            return 1.0

def calculate_tonnage(volume, density, temperature):
    """
    Calculate tonnage using the formula: tonnage = (volume * density * vcf) / 1000
    """
    vcf = get_vcf(density, temperature)
    tonnage = (volume * density * vcf) / 1000
    return tonnage, vcf

def home(request):
    """Home page with calculator form"""
    if request.method == 'POST':
        form = OilTonnageForm(request.POST)
        if form.is_valid():
            volume = form.cleaned_data['volume']
            density = form.cleaned_data['density']
            temperature = form.cleaned_data['temperature']
            
            # Calculate tonnage
            tonnage, vcf = calculate_tonnage(volume, density, temperature)
            
            # Save to database
            oil_tonnage = OilTonnage.objects.create(
                volume=volume,
                density=density,
                temperature=temperature,
                vcf=vcf,
                tonnage=tonnage
            )
            
            messages.success(request, f'Calculation completed successfully! Tonnage: {tonnage:.3f} MT')
            return redirect('calculator:home')
    else:
        form = OilTonnageForm()
    
    # Get recent calculations for display
    recent_calculations = OilTonnage.objects.all()[:5]
    
    context = {
        'form': form,
        'recent_calculations': recent_calculations,
    }
    return render(request, 'calculator/home.html', context)

def history(request):
    """Display calculation history with search and sort functionality"""
    calculations = OilTonnage.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        calculations = calculations.filter(
            Q(volume__icontains=search_query) |
            Q(density__icontains=search_query) |
            Q(temperature__icontains=search_query) |
            Q(tonnage__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['volume', 'density', 'temperature', 'vcf', 'tonnage', 'created_at']:
        calculations = calculations.order_by(sort_by)
    elif sort_by in ['-volume', '-density', '-temperature', '-vcf', '-tonnage', '-created_at']:
        calculations = calculations.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(calculations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'calculator/history.html', context)

def api_calculate(request):
    """API endpoint for AJAX calculations"""
    if request.method == 'POST':
        try:
            volume = float(request.POST.get('volume', 0))
            density = float(request.POST.get('density', 0))
            temperature = float(request.POST.get('temperature', 0))
            
            if volume <= 0 or density <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Volume and density must be greater than 0'
                })
            
            if temperature < -50 or temperature > 150:
                return JsonResponse({
                    'success': False,
                    'error': 'Temperature must be between -50°C and 150°C'
                })
            
            tonnage, vcf = calculate_tonnage(volume, density, temperature)
            
            return JsonResponse({
                'success': True,
                'tonnage': round(tonnage, 3),
                'vcf': round(vcf, 4),
                'rounded_density': round_to_nearest(density, 0.5),
                'rounded_temperature': round_to_nearest(temperature, 0.25)
            })
            
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'Invalid input values'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
