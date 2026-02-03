from django.contrib import admin
from .models import Medicamento
# Register your models here.

class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo_producto', 'descripcion_producto', 'farmacia', 'direccion', 'cantidad', 'fecha_actualizacion')