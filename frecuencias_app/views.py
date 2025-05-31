from django.shortcuts import render
from .forms import CargaArchivoForm
from .utils.procesamiento import leer_excel_columnas
from .utils.frecuencia import generar_tabla_frecuencia
from .utils.graficos import graficar_variable
from .utils.estadisticas import procesar_variable_cuantitativa
import os
from django.shortcuts import render, redirect
def index(request):
    contexto = {}
    if request.method == 'POST':
        form = CargaArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            tipo_variable = form.cleaned_data['tipo_variable']
            df, columnas = leer_excel_columnas(archivo)
            columna = request.POST.get('columna')

            if not columna:
                # Solo se subió el archivo, mostrar columnas
                contexto = {
                    'form': form,
                    'columnas': columnas,
                    'tipo_variable': tipo_variable,
                    'mensaje': 'Selecciona una columna para continuar.',
                }
                return render(request, 'index.html', contexto)

            # Ahora sí: procesar la columna elegida
            serie = df[columna]

            if tipo_variable == 'cuantitativa-continua':
                output_dir = os.path.join('frecuencias_app', 'static', 'graficos')
                resultado = procesar_variable_cuantitativa(df, columna, output_dir)
                contexto = {
                    'tabla': resultado["tabla_frecuencias"].to_html(),
                    'resumen': resultado["tabla_resultados"].to_html(),
                    'grafico_histograma': '/static/graficos/' + resultado["graficos"]["histograma"],
                    'grafico_poligono': '/static/graficos/' + resultado["graficos"]["poligono"],
                    'grafico_ojiva': '/static/graficos/' + resultado["graficos"]["ojiva"]
                }
                return render(request, 'resultado.html', contexto)
            else:
                # Modo cualitativo o discreto
                tabla = generar_tabla_frecuencia(serie, tipo_variable)
                grafico_url = graficar_variable(serie, tipo_variable, columna)
                contexto = {
                    'tabla': tabla.to_html(),
                    'grafico_url': grafico_url
                }
                return render(request, 'resultado.html', contexto)
    else:
        form = CargaArchivoForm()

    contexto['form'] = form
    return render(request, 'index.html', contexto)
