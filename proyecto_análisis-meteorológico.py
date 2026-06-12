import numpy as np
import pandas as pd

# ANÁLISIS DE DATOS METEOROLÓGICOS CON PANDAS Y NUMPY

# 1. Creación DataFrame 
ruta = "C:/Users/noeli/Desktop/Big Data IA/Numpy\Proyecto Análisis Meteorológico/datos_meteorologicos.csv"
df = pd.read_csv(ruta)

# 2. Observaciones iniciales
print(df.info()) # Información general
print(df.shape) # El DataFrame tiene 5110 filas y 4 columnas (fecha, temperatura, precipitación y humedad)
print(df.describe()) # Nos permite conocer algunos valores estadísticos
print(df.dtypes) # Tiene 1 columna con datos tipo object (str) y 3 columnas con datos tipo float.
print(df.isnull().sum()) # Nos muestra que en cada columna, a excepción de fecha, hay 255 registros con datos NaN, lo cual sugiere que
# hay fechas que no se han registrado valores -> lo gestionaremos más adelante.
print(df.duplicated().sum()) # Nos muestra que hay 0 filas duplicadas, por lo que no hay que gestionar datos duplicados.

# 3. Convertir la fecha al tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")

# 4. Convertir las columnas del DataFrame en arrays de NumPy:
# Aquí solo convertimos las columnas numéricas en arrays, ya que fecha es de tipo object. Lo haremos de una en una:
temperatura = df["Temperatura"].to_numpy()
precipitacion = df["Precipitación"].to_numpy()
humedad = df["Humedad"].to_numpy()

# 5. Identificar los datos faltantes en los arrays y reemplazarlos por el promedio de los valores de cada columna
print(np.isnan(temperatura))
print(np.isnan(precipitacion))
print(np.isnan((humedad)))

# Generamos el promedio de cada array y reemplazamos los nan con este valor
promedio_temperatura = np.nanmean(temperatura)
promedio_precipitacion = np.nanmean(precipitacion)
promedio_humedad = np.nanmean(humedad)

temperatura_corregida = np.where(np.isnan(temperatura), promedio_temperatura, temperatura)
precipitacion_corregida = np.where(np.isnan(precipitacion), promedio_precipitacion, precipitacion)
humedad_corregida = np.where(np.isnan(humedad), promedio_humedad, humedad)

# 6. Análisis estadísticos
# 6.1 Temperatura promedio
temperatura_promedio = np.mean(temperatura_corregida)
print(f"La temperatura promedio es de {temperatura_promedio} grados")

# 6.2 Total de precipitaciones
total_precipitaciones = np.sum(precipitacion_corregida)
print(f"El total de precipitaciones es de {total_precipitaciones} litros")

# 6.3 Máxima humedad registrada
maxima_humedad = np.max(humedad_corregida)
print(f"La humedad máxima registrada es de {maxima_humedad} %")

# 6.4 Fecha más calurosa
fecha_mas_calurosa = df.loc[df["Temperatura"].idxmax(), "Fecha"]
print(f"La fecha más calurosa fue {fecha_mas_calurosa}")

# 6.5 Fecha más fría
fecha_mas_fria = df.loc[df["Temperatura"].idxmin(), "Fecha"]
print(f"La fecha más fría fue {fecha_mas_fria}")

# 6.6 Mediana y desviación típica de cada variable
mediana_temperatura = np.median(temperatura_corregida)
mediana_precipitacion = np.median(precipitacion_corregida)
mediana_humedad = np.median(humedad_corregida)

desviacion_temperatura = np.std(temperatura_corregida)
desviacion_precipitacion = np.std(precipitacion_corregida)
desviacion_humedad = np.std(humedad_corregida)

print(f"""Temperatura:
      - Mediana: {mediana_temperatura},
      - Desviación típica: {desviacion_temperatura}.
      Precipitación:
      - Mediana: {mediana_precipitacion},
      - Desviación típica: {desviacion_precipitacion}.
      Humedad:
      - Mediana: {mediana_humedad},
      - Desviación típica: {desviacion_humedad}.
      """)

# 6.7 Temperatura media mensual
df["Temperatura corregida"] = temperatura_corregida
df["Mes"] = df["Fecha"].dt.strftime("%m")
temperatura_media_mensual = df.groupby("Mes")["Temperatura corregida"].mean()
print(f"La temperatura media mensual es:\n {temperatura_media_mensual}")

# 6.8 Tabla comparativa de valores máximos de temperatura según el mes a lo largo de los años
df["Año"] = df["Fecha"].dt.strftime("%Y")
pivot = df.pivot_table(
    values=["Temperatura"],
    index="Año",
    columns="Mes",
    aggfunc="max",
)
print(f"Tabla comparativa temperaturas máximas:\n{pivot}")

# 7. Exportar los resultados a un nuevo archivo excel
# Aquí escribiremos mediante pd.ExcelWriter varias hojas en un mismo archivo, para lo cual necesitamos la librería openpyxl
# (por defecto, pandas la usa cuando llamamos to_excel)
resultados_generales = pd.DataFrame({"Métrica": ["Temperatura promedio", "Precipitación total", "Humedad máxima", 
                                                 "Día más caluroso", "Día más frío"]
                                    ,"Valores": [temperatura_promedio, total_precipitaciones, maxima_humedad, 
                                                 fecha_mas_calurosa, fecha_mas_fria]})

resultados_estadisticos = pd.DataFrame({"Métrica": ["Mediana", "Desviación típica"], 
                                        "Temperatura":[mediana_temperatura, desviacion_temperatura], 
                                        "Precipitación": [mediana_precipitacion, desviacion_precipitacion], 
                                        "Humedad":[mediana_humedad, desviacion_humedad]})

ruta_excel = "C:/Users/noeli/Desktop/Big Data IA/Numpy\Proyecto Análisis Meteorológico/datos_meteorologicos_tratados.xlsx"

with pd.ExcelWriter(ruta_excel) as writer:
    resultados_generales.to_excel(writer, sheet_name="Resumen datos generales", index=False)
    resultados_estadisticos.to_excel(writer, sheet_name="Datos estadísticos", index=False)
    pivot.to_excel(writer, sheet_name="Temperaturas max por mes y año")
    temperatura_media_mensual.to_excel(writer, sheet_name="Temperatura media mensual")

# Usamos with para evitar fallos inesperados que dejen el archivo abierto y corrupto antes de llegar a writer.close()
# con with, writer se cierra solo una vez acaba el bloque de código, y si se produce algún error, python cierra el archivo automáticamente
# antes de acabar el código.