from flask import request,jsonify

#pip install pandas
import pandas as pd
#pip install scikit-learn
#Instalando las Librerias Para Hacer nuestra Red Neuronal
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from utilitarios import generando_predicciones

#Creando la Aplicacion Back-End
from app import app

#Creando el Api Para Consumir por el Front
@app.route('/api/prediccion_ampaid',methods=['POST', 'GET'])
def predeccir():
    try:
        if request.method == 'POST':
            if request.is_json:
                datapost=request.get_json()
                # # Cargar los datos históricos de delitos
                data = pd.read_csv('datos_delincuencia3.csv',sep=";")
                # print(data.info()) #Si deseas ver el Tipo de Dato de los Campos
                # En este ejemplo,  ya se han limpiado y preparado los datos.
                # Dividir los datos en características (X) y etiquetas (y)
                X = data[['hora_robo', 'DiaDeLaSemana']]
                y = data['tipo_de_delito']

                #Dividir los datos en conjuntos de entrenamiento y prueba
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                #Crear un modelo de Random Forest Classifier
                modelo = RandomForestClassifier(n_estimators=100, random_state=42)

                #Entrenar el modelo
                modelo.fit(X_train, y_train)

                #Realizar predicciones en el conjunto de prueba
                y_pred = modelo.predict(X_test)

                #Evaluar el rendimiento del modelo
                accuracy = accuracy_score(y_test, y_pred)
                print(f"Precisión del modelo: {accuracy * 100:.2f}%")

                # Ahora puedes usar el modelo para predecir si ocurrirá un robo
                # hora = 14  # Hora del día (ejemplo)
                # dia_semana = 2  # Martes (ejemplo)

                # Ahora puedes usar el modelo para predecir si ocurrirá un robo debes pasarle la informacion desde el postman en formato JSON 
                """
                    {  "hora":14,
                        "diadelasemana":2
                    }
                """

                hora = datapost['hora']  # 14 Hora del día (ejemplo)
                dia_semana = datapost['diadelasemana'] #2  # Martes (ejemplo)
                latitud=str(datapost['latitud'])
                longitud=str(datapost['longitud'])
                slatitud=latitud[:6]
                slongitud=longitud[:6]


                nueva_entrada = [[hora, dia_semana]]
                prediccion = modelo.predict(nueva_entrada)
                if prediccion[0] == 1:
                    return jsonify({'datos': generando_predicciones(slatitud,slongitud)})
                else:
                    return {"datos": "nada que mostrar"}
    except :
        return {"datos": "parametos ingresados incorrectos"}


                    
##Test de Pruebas
    #http://127.0.0.1:5000/api/prediccion_ampaid
    #json
    """
    {  "hora":14,
     "diadelasemana":2
    }
    """
