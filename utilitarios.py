# Cargar los datos históricos de delitos
import pandas as pd

def generando_predicciones(lat,lon):
    data = pd.read_csv('datos_delincuencia3.csv',sep=";")
    pd_prediccion=data.query(f"data1=={lat} and data2 == {lon}")
    columnas_deseadas=["latitud","longitud","fecha_robo","id_urbanizacion","urbanizacion","id_criticidad","desc_criticidad","estado_criticidad"]
    pd_prediccion=pd_prediccion[columnas_deseadas]

    lista=pd_prediccion.to_dict(orient='records')
    return lista
    

#print(generando_predicciones(-12.05,-77.06))