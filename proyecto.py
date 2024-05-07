from flask import Flask,render_template,request,redirect,url_for
import mysql.connector as mysql
import random



def pedirPreguntasTrivialhp(numero_preguntas=10):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    cursor.execute("SELECT `pregunta`, `respuesta_correcta`, `respuesta_incorrecta1`,` respuesta_incorrecta2`,` respuesta_incorrecta3` FROM `trivial_preguntas_generales_hp`LIMIT %s;", (numero_preguntas,))
    listaPreguntas = cursor.fetchall()
    cursor.close()
    bd.close()
    return listaPreguntas
    
   
   
def obtenerPreguntaTrivialhp():
    listadoPreguntas=pedirPreguntasTrivialhp()
    for i in range(listadoPreguntas.Length):
        preguntaRandom=listadoPreguntas[i]
        pregunta=preguntaRandom[0]
        respuestas= [preguntaRandom[1],preguntaRandom[2],preguntaRandom[3],preguntaRandom[4]]
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
    respuestaOK=respuesta[0][0]
    if respuestaUsuario==respuestaOK:
        return True
    else:
        return False
    
def obtener_preguntas_test(numero_preguntas=10):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    cursor=bd.cursor()
    cursor.execute("SELECT * FROM TEST_Casas ORDER BY RAND() LIMIT %s", (numero_preguntas,))
    preguntas = cursor.fetchall()
    cursor.close()
    return preguntas
    

app= Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/trivialHP')
def trivialHP():
    return render_template('registrarUsuarioTrivial.html')


@app.route('/jugartrivialHP',methods=["GET","POST"])
def registrarUsuario():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    
    if request.method=="POST":
        registrar=request.form
        usuario=registrar.get('name')

        query=f"SELECT COUNT(*) FROM `resultados_hp_test` WHERE `nombre`= '{usuario}';"
        cursor.execute(query)
        result= cursor.fetchone()
        usuarioYaRegistrado=result[0]>0
        
        if not usuarioYaRegistrado:
            query=f"INSERT INTO `resultados_hp_test`( `nombre`, `aciertos`, `errores`) VALUES ('{usuario}',0,0);"
            cursor.execute(query)
            bd.commit()
            
        bd.close()
        return redirect(url_for('jugarTrivialHP',usuario=usuario))
  
@app.route('/jugarTrivialHP/<usuario>', methods=["GET","POST"])

def jugarTrivialHP(usuario):
    print('funcion llamada')
    num_preguntas=5
    contador_preguntas=int(request.args.get('contador_preguntas',0))
    print('Inicio:',contador_preguntas)
    
    if contador_preguntas<num_preguntas:
        if request.method=="GET":
            pregunta,respuesta1,respuesta2,respuesta3,respuesta4=obtenerPreguntaTrivialhp()
            contador_preguntas+=1
            print('pregunta sumada:',contador_preguntas)
            return render_template('trivialHarryPotter.html', preguntaHtml=pregunta,respuesta1Html=respuesta1,respuesta2Html=respuesta2,respuesta3Html=respuesta3,respuesta4Html=respuesta4,usuario=usuario, contador_preguntas=contador_preguntas)
      
        elif request.method=="POST":
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
            
            contador_preguntas+=1
            print('pregunta sumada:',contador_preguntas)
            
            return redirect(url_for('jugarTrivialHP', usuario=usuario,contador_preguntas=contador_preguntas))
         
    else:    
        return redirect(url_for('resultadoTrivial',usuario=usuario))
    
    

@app.route ('/resultadoTrivial',methods=["POST"])
def mostrarResultados(usuario):

    return render_template('resultadosTrivial.html',usuario=usuario)

@app.route('/testCasas', methods=["GET", "POST"])
def jugar_hp():
    if request.method == "GET":
        preguntas = obtener_preguntas_test()
        return render_template('testCasas.html', preguntas=preguntas)
    elif request.method == "POST":
        pregunta_id = request.form.get("pregunta_id")
        respuesta_seleccionada = request.form.get("respuesta")
        actualizar_resultado(respuesta_seleccionada)
        preguntas = obtener_preguntas_test()
        return render_template('testCasas.html', preguntas=preguntas)


def actualizar_resultado(respuesta_seleccionada):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    cursor = bd.cursor()
    cursor.execute(f"UPDATE resultados_hp_test SET total = total + 1 WHERE respuesta_correcta = '{respuesta_seleccionada}'")
    bd.commit()
    cursor.close()

@app.route('/calcular_casa', methods=["POST"])
def calcular_casa():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    casa = request.form.get("casa")
    cursor = bd.cursor()
    cursor.execute(f"INSERT INTO estudiantes_casas (ID, CASA) VALUES (NULL, '{casa}')")
    bd.commit()
    cursor.close()
    return "Casa calculada con éxito."

@app.route('/estudiantesCasas',methods=["GET","POST"])
def calculasEstudiantes():
    return

app.run()
