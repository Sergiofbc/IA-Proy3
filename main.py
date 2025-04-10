import subprocess
import sys
import os
import time

def instalar_dependencias():
    print("🔧 Verificando e instalando dependencias necesarias...")
    
    # Lista de paquetes requeridos
    requerimientos = [
        "numpy>=1.20.0",
        "pandas>=1.2.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
        "scikit-learn>=0.24.0"
    ]
    
    # Crear o actualizar requirements.txt
    with open("requirements.txt", "w") as f:
        for req in requerimientos:
            f.write(f"{req}\n")
    
    print("📝 Archivo requirements.txt creado/actualizado")
    
    # Intentar instalar los paquetes
    try:
        print("⏳ Instalando dependencias (esto puede tardar unos minutos)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def analisis_depresion():
    """Función principal para análisis del dataset de depresión en estudiantes"""
    # Importamos las librerías necesarias
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
    except ImportError as e:
        print(f"❌ Error al importar las librerías: {e}")
        print("Por favor, ejecuta el script nuevamente o instala las dependencias manualmente")
        return

    def crear_histogramas(df, carpeta_destino="histogramas"):
        # Crear carpeta si no existe
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
            print(f"✅ Carpeta '{carpeta_destino}' creada")
        
        # Definir columnas por tipo
        columnas_categoricas = ['Gender', 'Dietary Habits', 'Degree', 
                              'Have you ever had suicidal thoughts ?', 
                              'Family History of Mental Illness']
        
        columnas_numericas = ['Age', 'Academic Pressure', 'Work Pressure', 
                            'Study Satisfaction', 'Sleep Duration', 
                            'Work/Study Hours', 'Financial Stress']
        
        # Para columnas categóricas, crear gráficos de barras (una forma de histograma para datos categóricos)
        print("\n📊 Creando histogramas para variables categóricas...")
        for col in columnas_categoricas:
            if col in df.columns:
                plt.figure(figsize=(10, 6))
                # Contar valores y ordenar para mejor visualización
                value_counts = df[col].value_counts().sort_index()
                ax = sns.barplot(x=value_counts.index, y=value_counts.values)
                plt.title(f'Distribución de {col}')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                # Guardar gráfico
                ruta_archivo = os.path.join(carpeta_destino, f'histograma_{col.replace("/", "_").replace(" ", "_").replace("?", "")}.png')
                plt.savefig(ruta_archivo)
                plt.close()
                print(f"  - Histograma para '{col}' guardado")
        
        # Para columnas numéricas, crear histogramas
        print("\n📈 Creando histogramas para variables numéricas...")
        for col in columnas_numericas:
            if col in df.columns:
                plt.figure(figsize=(10, 6))
                sns.histplot(df[col].dropna(), kde=True)
                plt.title(f'Distribución de {col}')
                plt.tight_layout()
                # Guardar gráfico
                ruta_archivo = os.path.join(carpeta_destino, f'histograma_{col.replace("/", "_").replace(" ", "_")}.png')
                plt.savefig(ruta_archivo)
                plt.close()
                print(f"  - Histograma para '{col}' guardado")
        
        print(f"\n✅ Todos los histogramas han sido guardados en la carpeta '{carpeta_destino}'")

    # Cargar datos del archivo específico con codificación UTF-8
    archivo_csv = "student_depression_dataset.csv"
    try:
        # Especificar encoding='utf-8' para asegurar la correcta lectura de caracteres especiales
        df = pd.read_csv(archivo_csv, encoding='utf-8')
        print(f"✅ Archivo '{archivo_csv}' cargado correctamente con codificación UTF-8")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_csv}'")
        print("Asegúrate de que el archivo esté en el mismo directorio que este script")
        return
    except UnicodeDecodeError:
        # Si falla con UTF-8, intentar con otras codificaciones comunes
        try:
            df = pd.read_csv(archivo_csv, encoding='latin-1')
            print(f"✅ Archivo '{archivo_csv}' cargado con codificación latin-1 (UTF-8 falló)")
        except Exception as e:
            print(f"❌ Error al cargar el archivo con codificaciones alternativas: {e}")
            return
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return

    # Mostrar nombres de columnas
    print("\n🧾 Columnas del dataset:")
    for col in df.columns:
        print(f"- {col}")

    # Mostrar tipos de datos
    print("\n📘 Tipos de datos:")
    print(df.dtypes)

    # Ver valores nulos por columna
    print("\n🔍 Valores nulos por columna:")
    print(df.isnull().sum())

    # Ver cantidad de ceros por columna
    print("\n🧮 Cantidad de ceros por columna:")
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            print(f"{col}: {(df[col] == 0).sum()}")

    # Sugerencia de columnas a eliminar ya que no tienen ningún valor relevante
    columnas_a_eliminar = ['CGPA', 'Job Satisfaction']
    print("\n🗑️ Columnas que se eliminarán:")
    print(columnas_a_eliminar)

    # Eliminar columnas
    df = df.drop(columns=columnas_a_eliminar)

    # Mostrar las primeras filas del dataset limpio
    print("\n✅ Dataset limpio (primeras filas):")
    print(df.head())
    
    # Crear histogramas y guardarlos en carpeta
    carpeta_destino = "histogramas"
    crear_histogramas(df, carpeta_destino)

def main():
    print("🚀 Iniciando programa de análisis de depresión en estudiantes...")
    
    # Instalar dependencias si es necesario
    if instalar_dependencias():
        print("\n⏳ Preparando análisis...")
        time.sleep(1)  # Pequeña pausa para mejor legibilidad
        
        # Ejecutar el análisis
        analisis_depresion()
    else:
        print("\n❌ No se pudieron instalar todas las dependencias.")
        print("Sugerencia: Intenta instalarlas manualmente con:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
