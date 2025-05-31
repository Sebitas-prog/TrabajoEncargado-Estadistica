import pandas as pd
import numpy as np

def generar_tabla_frecuencia(serie, tipo):
    if tipo == 'cualitativa':
        conteo = serie.value_counts()
        total = conteo.sum()
        tabla = pd.DataFrame({
            'Categoría': conteo.index,
            'Frecuencia': conteo.values,
            'Frecuencia Relativa (%)': (conteo.values / total) * 100
        })
    else:  # Cuantitativa
        conteo, bins = np.histogram(serie.dropna(), bins=5)
        total = conteo.sum()
        intervalos = [f"{bins[i]:.2f} - {bins[i+1]:.2f}" for i in range(len(bins)-1)]
        tabla = pd.DataFrame({
            'Intervalo': intervalos,
            'Frecuencia': conteo,
            'Frecuencia Relativa (%)': (conteo / total) * 100
        })
    return tabla
