from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import OilTonnage

class OilTonnageForm(forms.ModelForm):
    volume = forms.FloatField(
        label='Volume (litres)',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter volume in litres',
            'step': '0.01',
            'min': '0'
        }),
        validators=[MinValueValidator(0.0, message="Volume must be greater than 0")]
    )
    
    density = forms.FloatField(
        label='Density (kg/m³)',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter density in kg/m³',
            'step': '0.1',
            'min': '0'
        }),
        validators=[MinValueValidator(0.0, message="Density must be greater than 0")]
    )
    
    temperature = forms.FloatField(
        label='Temperature (°C)',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter temperature in °C',
            'step': '0.1',
            'min': '-50',
            'max': '150'
        }),
        validators=[
            MinValueValidator(-50.0, message="Temperature must be at least -50°C"),
            MaxValueValidator(150.0, message="Temperature must be at most 150°C")
        ]
    )
    
    class Meta:
        model = OilTonnage
        fields = ['volume', 'density', 'temperature']
    
    def clean(self):
        cleaned_data = super().clean()
        volume = cleaned_data.get('volume')
        density = cleaned_data.get('density')
        temperature = cleaned_data.get('temperature')
        
        if volume is not None and volume <= 0:
            self.add_error('volume', 'Volume must be greater than 0')
        
        if density is not None and density <= 0:
            self.add_error('density', 'Density must be greater than 0')
        
        if temperature is not None and (temperature < -50 or temperature > 150):
            self.add_error('temperature', 'Temperature must be between -50°C and 150°C')
        
        return cleaned_data 