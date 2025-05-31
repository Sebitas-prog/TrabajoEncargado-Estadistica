from django.shortcuts import render
from .forms import CargaArchivoForm
from .utils.procesamiento import leer_excel_columnas
from .utils.frecuencia import generar_tabla_frecuencia
from .utils.graficos import graficar_variable

def index(request):
    contexto = {}
    if request.method == 'POST':
        form = CargaArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            tipo_variable = form.cleaned_data['tipo_variable']
            df, columnas = leer_excel_columnas(archivo)
            columna = request.POST.get('columna')

            if columna:
                serie = df[columna]
                tabla = generar_tabla_frecuencia(serie, tipo_variable)
                grafico_url = graficar_variable(serie, tipo_variable, columna)
                contexto = {
                    'form': form,
                    'columnas': columnas,
                    'columna_seleccionada': columna,
                    'tabla': tabla.to_html(classes='table'),
                    'grafico_url': grafico_url,
                    'tipo_variable': tipo_variable
                }
            else:
                contexto = {'form': form, 'columnas': columnas, 'mensaje': 'Selecciona una columna'}
    else:
        form = CargaArchivoForm()
    contexto['form'] = form
    return render(request, 'index.html', contexto)
