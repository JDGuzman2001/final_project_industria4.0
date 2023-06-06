import pandas as pd
import glob
import matplotlib.pyplot as plt
archivos_csv = glob.glob('*.csv')
cantidad_csv = len(archivos_csv)
days = str(cantidad_csv)
print("Cantidad de días:", cantidad_csv)

dataframes = []
for archivo in archivos_csv:
	df = pd.read_csv(archivo)
	dataframes.append(df)
# Concatenar todos los DataFrames en uno solo
df_completo = pd.concat(dataframes)
print(df_completo.describe())
# Convertir los valores de la columna "Hora" en valores numéricos
df_completo['Hora'] = df_completo['Hora'].astype(str).str.extract('(\d+)').astype(int)
# Ordenar el DataFrame por la columna "Hora"
df_completo = df_completo.sort_values('Hora')
# Obtener el número total de personas en cada hora
total_personas = df_completo.groupby('Hora')['Cantidad de Datos'].sum()
print("Total de personas por hora:")
print(total_personas)
# Obtener la hora con la mayor cantidad de personas
hora_max_personas = total_personas.idxmax()
print("La hora con la mayor cantidad de personas es:", hora_max_personas)
# Obtener la hora con la menor cantidad de personas
hora_min_personas = total_personas.idxmin()
print("La hora con la menor cantidad de personas es:", hora_min_personas)
# Calcular el promedio de cantidad de personas por hora
promedio_personas = df_completo.groupby('Hora')['Cantidad de Datos'].mean()
# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
bar_width = 0.5

plt.bar(promedio_personas.index, promedio_personas.values, width=bar_width)
plt.xlabel('Hora')
plt.ylabel('Cantidad de personas promedio en ' + days + ' días')
plt.xticks(promedio_personas.index, rotation='horizontal')
plt.show()
