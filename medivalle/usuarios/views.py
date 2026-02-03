from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Medicamento

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Paciente

# Vista del login
def login_view(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo_documento')
        numero = request.POST.get('numero_documento')

        try:
            paciente = Paciente.objects.get(tipo_documento=tipo, numero_documento=numero)
            # Si el usuario existe, lo redirige al home
            messages.success(request, f'Bienvenido {paciente.nombre_completo} 👋')
            return redirect('bienvenida', tipo_doc=tipo, num_doc=numero)
        except Paciente.DoesNotExist:
            messages.error(request, 'Usuario no registrado en la base de datos de FOMAG.')

    return render(request, 'usuarios/login.html')

# Vista de departamentos
from django.shortcuts import render, redirect
from django.contrib import messages

def bienvenida(request, tipo_doc, num_doc):
    departamentos = [
        'Amazonas', 'Antioquia', 'Arauca', 'Atlántico', 'Bolívar', 'Boyacá', 'Caldas', 'Caquetá',
        'Casanare', 'Cauca', 'Cesar', 'Chocó', 'Córdoba', 'Cundinamarca', 'Guainía', 'Guaviare',
        'Huila', 'La Guajira', 'Magdalena', 'Meta', 'Nariño', 'Norte de Santander', 'Putumayo',
        'Quindío', 'Risaralda', 'San Andrés y Providencia', 'Santander', 'Sucre', 'Tolima',
        'Valle del Cauca', 'Vaupés', 'Vichada'
    ]

    if request.method == 'POST':
        departamento = request.POST.get('departamento')
        if departamento:
            # Redirige a la vista de medicamentos
            return redirect('medicamentos', tipo_doc=tipo_doc, num_doc=num_doc, departamento=departamento)
        else:
            messages.error(request, 'Debe seleccionar un departamento.')

    context = {
        'tipo_doc': tipo_doc,
        'num_doc': num_doc,
        'departamentos': departamentos
    }

    return render(request, 'usuarios/bienvenida.html', context)


# Vista principal CRUD
def medicamentos(request, tipo_doc, num_doc, departamento):
    # Campos de búsqueda
    codigo = request.GET.get('codigo', '').strip()
    ciudad = request.GET.get('ciudad', '').strip()
    descripcion = request.GET.get('descripcion', '').strip()

    # Consulta base
    medicamentos = Medicamento.objects.all()

    # Aplicar filtros dinámicos
    if codigo:
        medicamentos = medicamentos.filter(codigo_producto__icontains=codigo)
    if ciudad:
        medicamentos = medicamentos.filter(ciudad__icontains=ciudad)
    if descripcion:
        medicamentos = medicamentos.filter(descripcion_producto__icontains=descripcion)

    # Registrar nuevo medicamento
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        gramaje = request.POST.get('gramaje')
        farmacia = request.POST.get('farmacia')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        cantidad = request.POST.get('cantidad')

        # Validar duplicados
        if Medicamento.objects.filter(codigo_producto=codigo_producto).exists():
            messages.error(request, f"El medicamento con código {codigo_producto} ya existe.")
        else:
            Medicamento.objects.create(
                codigo_producto=codigo_producto,
                descripcion_producto=descripcion_producto,
                gramaje=gramaje,
                farmacia=farmacia,
                direccion=direccion,
                ciudad=ciudad,
                cantidad=cantidad
            )
            messages.success(request, "Medicamento registrado correctamente ✅")
            return redirect('medicamentos', tipo_doc=tipo_doc, num_doc=num_doc, departamento=departamento)

    context = {
        'tipo_doc': tipo_doc,
        'num_doc': num_doc,
        'departamento': departamento,
        'medicamentos': medicamentos,
        'codigo': codigo,
        'ciudad': ciudad,
        'descripcion': descripcion
    }

    return render(request, 'usuarios/medicamentos.html', context)


# Editar medicamento
def editar_medicamento(request, tipo_doc, num_doc, departamento, codigo):
    medicamento = get_object_or_404(Medicamento, codigo_producto=codigo)

    if request.method == 'POST':
        medicamento.descripcion_producto = request.POST.get('descripcion_producto')
        medicamento.gramaje = request.POST.get('gramaje')
        medicamento.farmacia = request.POST.get('farmacia')
        medicamento.direccion = request.POST.get('direccion')
        medicamento.ciudad = request.POST.get('ciudad')
        medicamento.cantidad = int(request.POST.get('cantidad'))
        medicamento.save()
        messages.success(request, '✅ Medicamento actualizado correctamente.')
        return redirect('medicamentos', tipo_doc=tipo_doc, num_doc=num_doc, departamento=departamento)

    context = {
        'medicamento': medicamento,
        'tipo_doc': tipo_doc,
        'num_doc': num_doc,
        'departamento': departamento
    }
    return render(request, 'usuarios/editar_medicamento.html', context)


# Eliminar medicamento
def eliminar_medicamento(request, tipo_doc, num_doc, departamento, codigo):
    medicamento = get_object_or_404(Medicamento, codigo_producto=codigo)
    medicamento.delete()
    messages.warning(request, '🗑️ Medicamento eliminado correctamente.')
    return redirect('medicamentos', tipo_doc=tipo_doc, num_doc=num_doc, departamento=departamento)
