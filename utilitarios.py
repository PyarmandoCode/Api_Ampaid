import psycopg2
import pandas as pd

# Establecer la conexión a la base de datos PostgreSQL de Google Cloud
def conexion_postgress():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Jhonnell2023",
        host="34.136.193.201",
        port=5432
    )
    return conn


nombre_tabla = 'ampaid.t_hist_evento_delictivo'
consulta_sql = f"SELECT * FROM {nombre_tabla};"


def generando_predicciones(lat,lon,dia):
   try:
        #todo tomara la data que el modelo ha generado
        data = pd.read_sql_query(consulta_sql,conexion_postgress())

        # todo dandole un numero por dia de la semana
        days = {0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

        # todo creando el campo numero de la semana
        data['fecha_evento'] = pd.to_datetime(data['fecha_evento'])
        data['Numero_Del_Dia'] = data['fecha_evento'].dt.dayofweek
        data['DiaDeLaSemana'] = data['Numero_Del_Dia'].apply(lambda x: days[x])

        pd_prediccion = data[(data['latitud'].str.contains(lat)) & (data['longitud'].str.contains(lon))]
        pd_prediccion_dia = pd_prediccion.loc[pd_prediccion['Numero_Del_Dia'] == dia]

        #todo test_respectivos toda la prediccion
        print(pd_prediccion)
        # todo test_respectivos filtrado por fecha
        print(pd_prediccion_dia)
   except Exception as error:
       print(f"Ocurrio un Error",error)

   return pd_prediccion_dia

print(generando_predicciones('-77.0166','-12.051379',0))
#print(generando_predicciones('-12.044653','-77.054807'))
#print(generando_predicciones('-12.05','-77.06'))
