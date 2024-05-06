from flask import Flask,render_template,request
import mysql.connector as mysql
import random



def pedirPreguntasTrivialhp():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    query="SELECT `pregunta`, `respuesta_correcta`, `respuesta_incorrecta1`,` respuesta_incorrecta2`,` respuesta_incorrecta3` FROM `trivial_preguntas_generales_hp`;"
    cursor.execute(query)
    listaPreguntas=cursor.fetchall()
    bd.close()
    return listaPreguntas

def obtenerPreguntaTrivialhp():
    listadoPreguntas=pedirPreguntasTrivialhp()
    preguntasRandom=random.choice(listadoPreguntas)
    pregunta=preguntasRandom[0]
    respuestas= [preguntasRandom[1],preguntasRandom[2],preguntasRandom[3],preguntasRandom[4]]
    random.shuffle(respuestas)
    respuesta1= respuestas[0]
    respuesta2=respuestas[1]
    respuesta3=respuestas[2]
    respuesta4=respuestas[3]
    return pregunta,respuesta1,respuesta2,respuesta3,respuesta4

def comprobarResultadoTrivialhp(pregunta,respuestaUsuario):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    query=f"SELECT `respuesta_correcta` FROM `trivial_preguntas_generales_hp` where `pregunta`='{pregunta}';"
    cursor.execute(query)
    respuesta=cursor.fetchall()
    bd.close()
    if respuesta:
        respuestaOK=respuesta[0][0]
        print('Respuesta correcta: ',respuestaOK)
        print('Respuesta usuario: ',respuestaUsuario)
        

        if respuestaUsuario==respuestaOK:
            return True
        else:
            return False
    
    
def jugarTrivialHP(usuario=None):

    if request.method=="GET":
        if usuario is None:
            return render_template('registrarUsuario.html'),usuario
        
    
    else:
        for i in range(3):
            bd=mysql.connect(user="root",password="",host="127.0.0.1",
                        database="trivialhp")
            pregunta=request.form.get("pregunta")
            respuestaUsuario=request.form.get("respuesta")
            resultado=comprobarResultadoTrivialhp(pregunta,respuestaUsuario) 
            cursor=bd.cursor()

            if resultado==True:
                query=f"UPDATE `resultados_hp_test` SET `aciertos`=`aciertos`+1 WHERE `nombre`='{usuario}';"

            else:
                query=f"UPDATE `resultados_hp_test` SET `errores`=`errores`+1 WHERE `nombre`='{usuario}';"

            cursor.execute(query)
            bd.commit()
            bd.close()

            pregunta,respuesta1,respuesta2,respuesta3,respuesta4=obtenerPreguntaTrivialhp()
            return render_template('trivialHarryPotter.html', preguntaHtml=pregunta,respuesta1Html=respuesta1,respuesta2Html=respuesta2,respuesta3Html=respuesta3,respuesta4Html=respuesta4), usuario


app= Flask(__name__)

@app.route('/trivialHP')
def root():
    return render_template('registrarUsuario.html')


@app.route('/jugartrivialHP',methods=["GET","POST"])
def regristrarUsuario():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    
    if request.method=="POST":
        regristrar=request.form
        usuario=regristrar.get('name')

        query=f"SELECT COUNT(*) FROM `resultados_hp_test` WHERE `nombre`= '{usuario}';"
        cursor.execute(query)
        result= cursor.fetchone()
        usuarioYaRegistrado=result[0]>0
        
        if not usuarioYaRegistrado:
            query=f"INSERT INTO `resultados_hp_test`( `nombre`, `aciertos`, `errores`) VALUES ('{usuario}',0,0);"
            cursor.execute(query)
            bd.commit()
            
        bd.close()
        return jugarTrivialHP(usuario)
  
    return jugarTrivialHP()



app.run()
