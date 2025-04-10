import pandas as pd

def main():
    # Cargar datos
    df = pd.read_csv("nombre_de_tu_archivo.csv")

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

    # Sugerencia de columnas a eliminar ya que no tienen ningun valor relevante
    columnas_a_eliminar = ['CGPA', 'Job Satisfaction']
    print("\n Columnas que se eliminarán:")
    print(columnas_a_eliminar)

    # Eliminar columnas
    df = df.drop(columns=columnas_a_eliminar)

    # Mostrar las primeras filas del dataset limpio
    print("\n✅ Dataset limpio (primeras filas):")
    print(df.head())

if __name__ == "__main__":
    main()
