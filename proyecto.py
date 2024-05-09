from flask import Flask,render_template,request,redirect,url_for, session, Response
import mysql.connector as mysql
import random
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def pedirPreguntasTrivialhp(numero_preguntas=10):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    cursor.execute("SELECT `pregunta`, `respuesta_correcta`, `respuesta_incorrecta1`,` respuesta_incorrecta2`,` respuesta_incorrecta3` FROM `trivial_preguntas_generales_hp` ORDER BY RAND() LIMIT %s;", (numero_preguntas,))
    listaPreguntas = cursor.fetchall()
    cursor.close()
    bd.close()
    return listaPreguntas
    
   
   
def obtenerPreguntaTrivialhp(preguntasRandom):
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
app.secret_key='1234'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/trivialHP',methods=["GET","POST"])
def trivialHP():
    listaPreguntas=pedirPreguntasTrivialhp()
    session['preguntas']=listaPreguntas
    session['index']=0
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
    listaPreguntas=session.get('preguntas')
    indexPreguntas=session.get('index')
    # comprobación que los datos han sido dados de forma correcta
    print(listaPreguntas)
    print(indexPreguntas)
    if request.method=="GET":
        if indexPreguntas< int(len(listaPreguntas)):
            pregunta,respuesta1,respuesta2,respuesta3,respuesta4=obtenerPreguntaTrivialhp(listaPreguntas[indexPreguntas])
            session['index']=indexPreguntas + 1
            print(indexPreguntas)
            return render_template('trivialHarryPotter.html', preguntaHtml=pregunta,respuesta1Html=respuesta1,respuesta2Html=respuesta2,respuesta3Html=respuesta3,respuesta4Html=respuesta4,usuario=usuario)
        
        else:
            return  redirect(url_for('mostrarResultados', usuario=usuario)) 
    
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
    
        return redirect(url_for('jugarTrivialHP',usuario=usuario))
        
  
       
      
    
    

@app.route ('/resultadoTrivial/<usuario>',methods=["GET","POST"])
def mostrarResultados(usuario):
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    query=f"SELECT `aciertos` FROM `resultados_hp_test` where `nombre`='{usuario}';"
    cursor.execute(query)
    aciertos=cursor.fetchone()
    query=f"SELECT `errores` FROM `resultados_hp_test` where `nombre`='{usuario}';"
    cursor.execute(query)
    errores=cursor.fetchone()
    bd.close()
    return "aquí irán los resultados del juego para el usuario: "+usuario
    # return render_template('resultadoTrivial.html',usuario=usuario, aciertos=aciertos,errores=errores)



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
def calcularEstudiantes():
    bd=mysql.connect(user="root",password="",host="127.0.0.1",
                     database="trivialhp")
    cursor=bd.cursor()
    query="SELECT `numEstudiantes`  FROM `estudiantes_casas` WHERE `casa`='Gryffindor';"
    cursor.execute(query)
    gryffindor=cursor.fetchone()
    query="SELECT `numEstudiantes`  FROM `estudiantes_casas` WHERE `casa`='Slytherin';"
    cursor.execute(query)
    slytherin=cursor.fetchone()
    query="SELECT `numEstudiantes`  FROM `estudiantes_casas` WHERE `casa`='Ravenclaw';"
    cursor.execute(query)
    ravenclaw=cursor.fetchone()
    query="SELECT `numEstudiantes`  FROM `estudiantes_casas` WHERE `casa`='Hufflepuff';"
    cursor.execute(query)
    hufflepuff=cursor.fetchone()
    bd.close()
    df =pd.DataFrame({
        'Gryffindor': gryffindor,
        'Slytherin': slytherin,
        'RavenClaw' : ravenclaw,
        'Hufflepuff' : hufflepuff
    })
    df.plot(figsize=(10,8), title='Estudiantes Casas', kind='bar', stacked=False)
    output=io.BytesIO()
    plt.savefig(output,format="png")
    # grafico= Response(output.getvalue(), mimetype='image/png')
    
    return Response(output.getvalue(), mimetype='image/png')



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


app.run(debug=True)
