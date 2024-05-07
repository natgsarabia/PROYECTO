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
    cursor.execute("SELECT * FROM TEST_Casas ORDER BY RAND() LIMIT %s", (numero_preguntas,))
    preguntas = cursor.fetchall()
    cursor.close()
    bd.close()
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
def jugar_test():
    if request.method == "GET":
        preguntas = obtener_preguntas_test()
        return render_template('testCasas.html', preguntas=preguntas)
    elif request.method == "POST":
        pregunta_id = request.form.get("pregunta_id")
        respuesta_seleccionada = request.form.get("respuesta")
        actualizar_resultado(pregunta_id, respuesta_seleccionada)
        preguntas = obtener_preguntas_test()
        return render_template('testCasas.html', preguntas=preguntas)


def actualizar_resultado(pregunta_id, respuesta_seleccionada):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    cursor.execute(f"SELECT respuesta_correcta FROM TEST_Casas WHERE id = {pregunta_id}")
    respuesta_correcta = cursor.fetchone()[0]
    if respuesta_seleccionada == respuesta_correcta:  
        cursor.execute(f"UPDATE Resultados_HP_TEST SET aciertos = aciertos + 1 WHERE id = 1")
    else:
        cursor.execute(f"UPDATE Resultados_HP_TEST SET errores = errores + 1 WHERE id = 1")
    bd.commit()
    cursor.close()

@app.route('/calcular_casa', methods=["POST"])
def calcular_casa():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    casa = request.form.get("respuesta")
    cursor = bd.cursor()
    cursor.execute(f"INSERT INTO estudiantes_casas (casa) VALUES ('{casa}')")
    bd.commit()
    bd.close()
    return redirect(url_for('porcentajeCasas'))
    

@app.route('/estudiantesCasas',methods=["GET","POST"])
def calculasEstudiantes():
    return



@app.route('/porcentajeCasas', methods=["GET", "POST"])
def porcentajeCasas():
    bd = mysql.connect(user="root", password="", host="127.0.0.1", database="trivialhp")
    cursor = bd.cursor()
    cursor.execute("SELECT COUNT(*) FROM estudiantes_casas WHERE casa='Griffindor'")
    griffindor = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM estudiantes_casas WHERE casa='Hufflepuff'")
    hufflepuff = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM estudiantes_casas WHERE casa='Ravenclaw'")
    ravenclaw = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM estudiantes_casas WHERE casa='Slytherin'")
    slytherin = cursor.fetchone()[0]
    total_estudiantes = griffindor + hufflepuff + ravenclaw + slytherin
    porcentaje_griffindor = (griffindor / total_estudiantes) * 100 if total_estudiantes != 0 else 0
    porcentaje_hufflepuff = (hufflepuff / total_estudiantes) * 100 if total_estudiantes != 0 else 0
    porcentaje_ravenclaw = (ravenclaw / total_estudiantes) * 100 if total_estudiantes != 0 else 0
    porcentaje_slytherin = (slytherin / total_estudiantes) * 100 if total_estudiantes != 0 else 0
    cursor.execute("INSERT INTO porcentajeCasas (Griffindor, Hufflepuff, Ravenclaw, Slytherin) VALUES (%s, %s, %s, %s)", 
                   (porcentaje_griffindor, porcentaje_hufflepuff, porcentaje_ravenclaw, porcentaje_slytherin))
    bd.commit()
    bd.close()
    return redirect(url_for('mostrarPorcentaje'))

@app.route('/mostrarPorcentaje')
def mostrarPorcentaje():
    bd = mysql.connect(user="root", password="", host="127.0.0.1", database="trivialhp")
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM porcentaje_Casas") 
    porcentajes = cursor.fetchone()
    bd.close()
    return render_template('porcentajeCasas.html', porcentajes=porcentajes)

@app.route('/porcentajeCasas')
def porcentajeCasas():
    return mostrarPorcentaje()


app.run()
