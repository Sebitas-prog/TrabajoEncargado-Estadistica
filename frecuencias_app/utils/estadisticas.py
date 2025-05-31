import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

def procesar_variable_cuantitativa(df, columna, output_dir):
    if columna not in df.columns:
        return {"error": f"La columna '{columna}' no existe."}

    vector = df[columna].dropna()

    if not np.issubdtype(vector.dtype, np.number):
        return {"error": f"La columna '{columna}' no es numérica."}

    # Contar decimales
    contar_decimales = lambda x: 0 if x % 1 == 0 else len(str(x).split('.')[-1].rstrip('0'))
    decimales = max(vector.map(contar_decimales))

    n = len(vector)
    maximo = vector.max()
    minimo = vector.min()
    rango = maximo - minimo

    # Número de clases
    m_raw = 1 + 3.3 * np.log10(n)
    m = round(m_raw) if (m_raw % 1 != 0.5 or int(m_raw) % 2 != 0) else int(m_raw)
    m = int(m)

    # Amplitud
    decimales_amp = decimales + 1
    amplitud = np.ceil((rango / m) * 10**decimales_amp) / 10**decimales_amp

    # Límites
    li = np.arange(minimo, minimo + m * amplitud, amplitud)
    ls = li + amplitud
    breaks = np.append(li, ls[-1])

    # Frecuencias
    frecuencia, _ = np.histogram(vector, bins=breaks)
    frecuencia_acum = np.cumsum(frecuencia)
    frecuencia_rel = frecuencia / n
    marca_clase = (li + ls) / 2

    # Tabla de frecuencias
    tabla_frec = pd.DataFrame({
        'Clase': [f"[{round(a,2)} - {round(b,2)})" for a, b in zip(li, ls)],
        'Marca de clase': marca_clase,
        'Frecuencia': frecuencia,
        'Frecuencia Acumulada': frecuencia_acum,
        'Frecuencia Relativa': frecuencia_rel
    })

    # Estadísticas
    media = np.sum(marca_clase * frecuencia) / n

    pos_mediana = n / 2
    idx_m = np.where(frecuencia_acum >= pos_mediana)[0][0]
    Lm = li[idx_m]
    F_prev = frecuencia_acum[idx_m - 1] if idx_m > 0 else 0
    fm = frecuencia[idx_m]
    mediana = Lm + ((pos_mediana - F_prev) / fm) * amplitud

    idx_moda = np.argmax(frecuencia)
    Lmo = li[idx_moda]
    f1 = frecuencia[idx_moda]
    f0 = frecuencia[idx_moda - 1] if idx_moda > 0 else 0
    f2 = frecuencia[idx_moda + 1] if idx_moda + 1 < len(frecuencia) else 0
    moda = Lmo + ((f1 - f0) / ((f1 - f0) + (f1 - f2))) * amplitud if (f1 - f0 + f1 - f2) != 0 else Lmo

    varianza = np.sum(((marca_clase - media) ** 2) * frecuencia) / (n - 1)
    desviacion = np.sqrt(varianza)
    cv = (desviacion / media) * 100

    tabla_resumen = pd.DataFrame({
        'Medida': ["Media", "Mediana", "Moda", "Rango", "Varianza", "Desviación estándar", "Coef. de variación (%)"],
        'Valor': [media, mediana, moda, rango, varianza, desviacion, cv]
    })

    # Guardar gráficos
    def guardar_grafico(fig, nombre):
        path = os.path.join(output_dir, f"{uuid.uuid4().hex}_{nombre}.png")
        fig.savefig(path, bbox_inches='tight')
        plt.close(fig)
        return os.path.basename(path)

    fig1, ax1 = plt.subplots()
    ax1.bar(marca_clase, frecuencia, width=amplitud * 0.9, color='skyblue', edgecolor='black')
    ax1.set_title("Histograma de frecuencias")
    ax1.set_xlabel(columna)
    ax1.set_ylabel("Frecuencia")
    img_histograma = guardar_grafico(fig1, "histograma")

    fig2, ax2 = plt.subplots()
    ax2.plot(marca_clase, frecuencia, marker='o', color='darkred')
    ax2.set_title("Polígono de frecuencias")
    ax2.set_xlabel(columna)
    ax2.set_ylabel("Frecuencia")
    img_poligono = guardar_grafico(fig2, "poligono")

    fig3, ax3 = plt.subplots()
    ax3.plot(ls, frecuencia_acum / n * 100, marker='o', color='darkgreen')
    ax3.set_title("Ojiva")
    ax3.set_xlabel(columna)
    ax3.set_ylabel("Frecuencia acumulada (%)")
    ax3.set_ylim(0, 100)
    img_ojiva = guardar_grafico(fig3, "ojiva")

    return {
        "tabla_frecuencias": tabla_frec,
        "tabla_resultados": tabla_resumen,
        "graficos": {
            "histograma": img_histograma,
            "poligono": img_poligono,
            "ojiva": img_ojiva
        }
    }
