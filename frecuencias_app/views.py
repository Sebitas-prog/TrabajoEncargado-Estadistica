from django.shortcuts import render
from .forms import CargaArchivoForm
from .utils.procesamiento import leer_excel_columnas
from .utils.frecuencia import generar_tabla_frecuencia
from .utils.graficos import graficar_variable
from .utils.estadisticas import procesar_variable_cuantitativa  # NUEVO

import os

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

                if tipo_variable == 'cuantitativa-continua':
                    output_dir = os.path.join('frecuencias_app', 'static', 'graficos')
                    os.makedirs(output_dir, exist_ok=True)

                    resultado = procesar_variable_cuantitativa(df, columna, output_dir)

                    if 'error' in resultado:
                        contexto = {'form': form, 'columnas': columnas, 'mensaje': resultado['error']}
                    else:
                        contexto = {
                            'form': form,
                            'columnas': columnas,
                            'columna_seleccionada': columna,
                            'tabla': resultado["tabla_frecuencias"].to_html(classes='table'),
                            'resumen': resultado["tabla_resultados"].to_html(classes='table table-bordered'),
                            'grafico_histograma': '/static/graficos/' + resultado["graficos"]["histograma"],
                            'grafico_poligono': '/static/graficos/' + resultado["graficos"]["poligono"],
                            'grafico_ojiva': '/static/graficos/' + resultado["graficos"]["ojiva"],
                            'tipo_variable': tipo_variable
                        }
                else:
                    # Modo anterior para cualitativa y cuantitativa-discreta
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
