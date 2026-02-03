from django.db import models
from django.utils import timezone

# Create your models here.
class Paciente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PA', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    regimen = models.CharField(max_length=50, default='FOMAG')

    def __str__(self):
        return f'{self.nombre_completo} ({self.tipo_documento} {self.numero_documento})'

class Medicamento(models.Model):
    codigo_producto = models.CharField(max_length=50, primary_key=True)
    descripcion_producto = models.TextField()
    gramaje = models.CharField(max_length=30, blank=True, null=True)
    farmacia = models.TextField()
    direccion = models.CharField(max_length=80)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def estado_color(self):
        if 10 <= self.cantidad <= 50:
            return ('Parcial', 'warning')  # amarillo
        elif 0 <= self.cantidad <= 9:
            return ('Agotado', 'danger')  # rojo
        elif self.cantidad >= 51:
            return ('Disponible', 'success')  # verde
        return ('Sin Estado', 'secondary')

    def __str__(self):
        return f"{self.codigo_producto} - {self.descripcion_producto}"