# Proyecto: Análisis de Datos Meteorológicos ⛅
Proyecto de análisis de datos meteorológicos usando las librerías Pandas y Numpy.

## ¿Qué pretende este proyecto?
Con este proyecto busco combinar los conocimientos adquiridos previamente en Pandas con los nuevos de NumPy para el tratamiento de datos y análisis estadístico.

## Resumen del proyecto:
Trabajo con un CSV (datos_meteorologicos.csv) que contiene los registros diarios de temperatura, precipitación y humedad entre 2010 y 2023. Hay varias fechas con ausencia de valores (NaN)
que mediante la limpieza posterior usando arrays de NumPy sustituyo por el valor promedio de la variable.

A continuación genero varios análisis estadísticos combinando ufuncs de NumPy y conocimientos previos de Pandas que incluyen:
- Temperatura promedio (np.mean()), total de precipitaciones (np.sum()) y máxima humedad registrada (np.max())
- Fecha más calurosa y fecha más fría (uso de loc y idxmax)
- Mediana y desviación típica de las variables (np.median() y np.std())
- Temperatura media mensual (groupby)
- Tabla comparativa de las temperaturas máximas de cada mes a lo largo de los años (pivot_table)

Esto genera una serie de datos que posteriormente exporto a un archivo excel con varias hojas a través de pd.ExcelWriter en un bloque de código with, el cual permite evitar fallos inesperados si ocurre algún error.

## Para ejecutar el script...
Se necesita tener un intérprete de python que contenga las librerías Pandas y Numpy, en mi caso yo uso conda (obtenible mediante la descarga de Anaconda)
Igualmente, para crear y escribir el excel usando el writer, se necesita tener la librería openpyxl, la cual usa por defecto Pandas (si no lo tienes, ejecuta conda install openpyxl en la terminal)


