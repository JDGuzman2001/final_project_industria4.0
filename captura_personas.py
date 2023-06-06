import pandas as pd
import time
import serial
import redis
tiempo_total = 85
intervalo = 5  # Intervalo de captura en segundos
r = redis.Redis(
host ='redis-10760.c15.us-east-1-2.ec2.cloud.redislabs.com',
port=10760,
password='97I2rWZNXuhJdXZ9haFONgAjLeewfTyu')
ts = r.ts()
#ts.create("Personas")
puerto = serial.Serial('COM8', 115200, timeout=0, rtscts=1)

num_filas = tiempo_total // intervalo
horas = range(6, 6 + num_filas)  # Nombres de las filas (horas)

data = {'Hora': [], 'Cantidad de Datos': []}

fila_actual = 6  # Fila actual para la captura
inicio_intervalo = time.time()
datos_capturados = set()
tiempo_actual = time.time()

while fila_actual <= num_filas + 5:
    z = puerto.readline().decode('ascii').strip()
    if tiempo_actual - inicio_intervalo < intervalo:
        if z:
            datos_capturados.add(z)
            try:
                ts.add("Personas", "*",z)
            except:
                print("error al enviar a redis")
    else:
        data['Hora'].append(fila_actual)
        data['Cantidad de Datos'].append(len(datos_capturados))
        datos_capturados = set()
        fila_actual += 1
        inicio_intervalo = time.time()

        print(f"Datos capturados en la fila {fila_actual-1}: {len(datos_capturados)}")

    tiempo_actual = time.time()

df = pd.DataFrame(data)  # Crear DataFrame a partir del diccionario

df.to_csv('csv_sensor.csv', index=False)  # Guardar el DataFrame en un archivo CSV

print("Proceso completado.")







