import matplotlib.pyplot as plt
import seaborn as sns
import os
import uuid

GRAFICOS_DIR = 'static/graficos'

if not os.path.exists(GRAFICOS_DIR):
    os.makedirs(GRAFICOS_DIR)

def graficar_variable(serie, tipo, nombre):
    nombre_archivo = f"{uuid.uuid4().hex}.png"
    ruta = os.path.join(GRAFICOS_DIR, nombre_archivo)
    fig, ax = plt.subplots()

    if tipo == 'cualitativa':
        serie.value_counts().plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
    else:
        sns.histplot(serie.dropna(), kde=True, ax=ax)

    plt.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)
    return f"/static/graficos/{nombre_archivo}"
