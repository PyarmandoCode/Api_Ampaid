from flask import request,jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from utilitarios import generando_predicciones,conexion_postgress
from app import app

@app.route('/api/prediccion_ampaid',methods=['POST'])
def predeccir():
    try:
        nombre_tabla = 'ampaid.t_hist_evento_delictivo'
        consulta_sql = f"SELECT * FROM {nombre_tabla};"
        if request.method == 'POST':
            if request.is_json:
                datapost=request.get_json()
                # todo  1.- RECOPILAR LOS DATOS
                data = pd.read_sql_query(consulta_sql,conexion_postgress())

                #todo En este ejemplo,  ya se han limpiado y preparado los datos.
                #todo 2.- procesamiento de datos
                # Dividir los datos en características (X) y etiquetas (y)
                X = data[['id_evento', 'id_tipo_via']]
                y = data['delito']

                #todo 3 Dividir los datos en conjuntos de entrenamiento y prueba
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                #todo 4 este es la red neuronal

                modelo = RandomForestClassifier(n_estimators=100, random_state=42)

                #todo 4 es entrenar el modelo
                modelo.fit(X_train, y_train)

                #todo prediccion el modelo
                y_pred = modelo.predict(X_test)

                #todo 4 evaluas el rendimeinto del modelo
                accuracy = accuracy_score(y_test, y_pred)
                print(f"Precisión del modelo: {accuracy * 100:.2f}%")

                #todo parametros que se le pasa al modo
                dia_semana = datapost['diadelasemana']
                latitud=str(datapost['latitud'])
                longitud=str(datapost['longitud'])

                slatitud = latitud[:6]
                slongitud = longitud[:6]

                nueva_entrada = [[0, dia_semana]]
                prediccion = modelo.predict(nueva_entrada)
                #todo si devuelve uno se produzco el delito
                if prediccion[0] == 1:
                    datos_json= generando_predicciones(slatitud,slongitud,dia_semana)

                    #todo mostrar las columnas en el JSON

                    columnas_deseadas = ["latitud", "longitud", "fecha_evento", "id_evento","desc_tipo_evento",
                                         "id_tipo_via", "tipo_via", "nombre_via","nro_cuadra","Numero_Del_Dia"]

                    # todo el nuevo modelo prediciendo los datos
                    pd_prediccion_nuevo = datos_json[columnas_deseadas]

                    #todo modificando el formato de fecha mm/dd/yyyy

                    pd_prediccion_nuevo['fecha_evento'] = pd.to_datetime(datos_json['fecha_evento'])
                    pd_prediccion_nuevo['fecha_evento'] = pd_prediccion_nuevo['fecha_evento'].dt.strftime('%d-%m-%Y')

                    #todo convirtiendo los datos del modelo a JSON
                    pd_json = pd_prediccion_nuevo.to_dict(orient='records')
                    return jsonify({"datos":pd_json})
                else:
                    return {"datos": "nada que mostrar"}
    except  Exception as  error:
        return {"datos": error}
