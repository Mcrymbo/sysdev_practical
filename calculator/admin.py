from django.contrib import admin
from .models import VCFTable, OilTonnage

@admin.register(VCFTable)
class VCFTableAdmin(admin.ModelAdmin):
    list_display = ['density', 'temperature', 'vcf']
    list_filter = ['density', 'temperature']
    search_fields = ['density', 'temperature', 'vcf']
    ordering = ['density', 'temperature']
    list_per_page = 50

@admin.register(OilTonnage)
class OilTonnageAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'volume', 'density', 'temperature', 'vcf', 'tonnage']
    list_filter = ['created_at', 'density', 'temperature']
    search_fields = ['volume', 'density', 'temperature', 'tonnage']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Input Values', {
            'fields': ('volume', 'density', 'temperature')
        }),
        ('Calculated Results', {
            'fields': ('vcf', 'tonnage', 'created_at'),
            'classes': ('collapse',)
        }),
    )
