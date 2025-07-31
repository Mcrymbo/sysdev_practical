from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class VCFTable(models.Model):
    """
    Volume Correction Factor table with density and temperature indexing
    """
    density = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Density in kg/m³ (rounded to nearest 0.5)"
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(-50.0), MaxValueValidator(150.0)],
        help_text="Temperature in °C (rounded to nearest 0.25)"
    )
    vcf = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Volume Correction Factor"
    )
    
    class Meta:
        unique_together = ['density', 'temperature']
        indexes = [
            models.Index(fields=['density', 'temperature']),
        ]
    
    def __str__(self):
        return f"Density: {self.density} kg/m³, Temp: {self.temperature}°C, VCF: {self.vcf}"

class OilTonnage(models.Model):
    """
    Oil tonnage calculation results
    """
    volume = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Volume in litres"
    )
    density = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Density in kg/m³"
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(-50.0), MaxValueValidator(150.0)],
        help_text="Temperature in °C"
    )
    vcf = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Volume Correction Factor used"
    )
    tonnage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Calculated tonnage in MT"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.tonnage:.3f} MT - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
