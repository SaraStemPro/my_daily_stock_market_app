from alpha_vantage.timeseries import TimeSeries
from flask import render_template, request, redirect, url_for, flash, session
from .models import DBManager
from . import app
import pandas as pd
import os
from datetime import date
import investpy
from googletrans import Translator, constants
from deep_translator import GoogleTranslator
import smtplib

email_admin = os.environ.get("ADMIN_EMAIL")
password_admin = os.environ.get("ADMIN_PASSWORD")
server = os.environ.get("SERVER_EMAIL")
api_alpha = os.environ.get('API_ALPHA')

clave_acceso = os.urandom(12).hex()
ruta = 'aplicacion/data/sara_app.db'
db = DBManager(ruta)
db.conectar_sqlite('''CREATE TABLE IF NOT EXISTS favoritos(
        id integer PRIMARY KEY,
        name text NOT NULL)''')

translator = Translator()
dato_hoy = date.today()
hoy = dato_hoy.strftime("%d/%m/%Y")

def comprobar_usuario():
    email = request.args.get('email')
    users = db.consultarConSQL('SELECT user_email FROM users')
    emails = []
    for user in users:
        emails.append(user['user_email'])
    if email in emails:
        return True
    else:
        return False

def comprobar_usuario_clave():
    email = request.args.get('email')
    users = db.consultarConSQL('SELECT user_email FROM users')
    clave = db.consultarConSQL('SELECT clave FROM users where user_email="{}"'.format(email))
    emails = []
    for user in users:
        emails.append(user['user_email'])
    for i in clave:
        clave_ = i['clave']
    if email in emails and clave_ != "0":
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        flash("Ya has iniciado sesión.", "exito")
    else:
        return render_template("index.html")
    return render_template("index.html", email=email)


@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    email = request.args.get('email')
    usuario = comprobar_usuario()
    if usuario == True:
        sent_from = email_admin
        to = [request.args.get('email')]
        subject = 'Clave de acceso'
        body = 'Tu clave de acceso a la app My Daily Stock Market es: {}'.format(clave_acceso)
        email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, to, subject, body)
        try:
            smtp_server = smtplib.SMTP_SSL(server, 465)
            smtp_server.ehlo()
            smtp_server.login(email_admin, password_admin)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
        except Exception as ex:
            print("Something went wrong….", ex)
        return render_template("usuario.html", email=email)
    else:
        flash(email, "error")
        flash("No estás autorizad@ para interactuar con esta aplicación.", "error")
        flash("Por favor, contacta con el administrador para registrarte formalmente.", "error")
        return render_template("index.html", email=email)


@app.route('/contenido',  methods=['GET', 'POST'])
def listado_contenido():
    email = request.args.get('email')
    if request.args.get('contraseña'):
        usuario = comprobar_usuario()
        if usuario == True:
            if request.args.get('contraseña') == clave_acceso:
                db.conectar_sqlite(
                    'UPDATE acciones SET Fecha = "{}"'.format(hoy))
                datos = db.consultarConSQL(
                    'SELECT * FROM acciones')
                db.conectar_sqlite(
                    'UPDATE users SET clave = "{}" WHERE user_email ="{}"'.format(clave_acceso,email))
                return render_template("contenido.html", datos=datos, Fecha=hoy, email=email)
            else:
                flash(email, "error")
                flash("Tu contraseña es incorrecta, inténtalo de nuevo.", "error")
                return render_template("index.html")
    else:
        email = request.args.get('email')
        usuario_clave = comprobar_usuario_clave()
        if usuario_clave == True:
            db.conectar_sqlite(
                    'UPDATE acciones SET Fecha = "{}"'.format(hoy))
            datos = db.consultarConSQL(
                    'SELECT * FROM acciones')
            return render_template("contenido.html", datos=datos, Fecha=hoy, email=email)
        else:
            return render_template("index.html")
    

@app.route('/add_favoritos', methods=['GET', 'POST'])
def lista_favoritos():
    favorito = request.args.get('favorito')
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        datos = db.consultarConSQL('SELECT name FROM favoritos')
        if not datos:
            db.conectar_sqlite(
                'INSERT INTO favoritos (name) values ("{}")'.format(favorito))
            db.conectar_sqlite(
                'UPDATE acciones SET Favorito=1 WHERE Ticker="{}"'.format(favorito))
        else:
            consulta_fav = db.consultarConSQL(
                'SELECT name FROM favoritos WHERE name="{}"'.format(favorito))
            if not consulta_fav:
                db.conectar_sqlite(
                    'INSERT INTO favoritos (name) values ("{}")'.format(favorito))
                db.conectar_sqlite(
                    'UPDATE acciones SET Favorito=1 WHERE Ticker="{}"'.format(favorito))
            return redirect(url_for("listado_contenido", favorito=favorito, email=email))
    else:
        return redirect(url_for("index", email=email))


@app.route('/elim_favorito', methods=['GET', 'POST'])
def elimina_fav():
    no_favorito = request.args.get('no_favorito')
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        db.conectar_sqlite(
            'DELETE FROM favoritos WHERE name="{}"'.format(no_favorito))
        db.conectar_sqlite(
            'UPDATE acciones SET Favorito=0 WHERE Ticker="{}"'.format(no_favorito))
        db.conectar_sqlite(
            'DELETE FROM new_fav WHERE name="{}"'.format(no_favorito))
        db.conectar_sqlite(
            'DELETE FROM new_fav_2 WHERE name="{}"'.format(no_favorito))
    return redirect(url_for("listado_contenido", no_favorito=no_favorito, email=email))


@app.route('/elim_fav_user', methods=['GET', 'POST'])
def elimina_fav_user():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        no_favorito_user = request.args.get('no_favorito')
    return render_template("elim_fav_user.html", no_favorito_user=no_favorito_user, email=email)


@app.route('/elim_favorito_fav', methods=['GET', 'POST'])
def elimina_fav_2():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        no_fav = request.args.get('no_fav')
        db.conectar_sqlite(
            'DELETE FROM favoritos WHERE name="{}"'.format(no_fav))
        db.conectar_sqlite(
            'UPDATE acciones SET Favorito=0 WHERE Ticker="{}"'.format(no_fav))
        db.conectar_sqlite(
            'DELETE FROM new_fav WHERE name="{}"'.format(no_fav))
        db.conectar_sqlite(
            'DELETE FROM new_fav_2 WHERE name="{}"'.format(no_fav))
    return redirect(url_for("obtener_favoritos", no_fav=no_fav, email=email))


@app.route('/favoritos', methods=['GET', 'POST'])
def obtener_favoritos():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        db.conectar_sqlite(
            'CREATE TABLE IF NOT EXISTS new_fav (id INTEGER PRIMARY KEY AUTOINCREMENT, Fecha TEXT, País TEXT, Nombre TEXT, name TEXT, Soporte_Stop TEXT, Objetivo_1 TEXT, Objetivo_2 TEXT)')
        db.conectar_sqlite(
            'CREATE TABLE IF NOT EXISTS new_fav_2 AS SELECT id, Fecha, País, Nombre, name, Soporte_Stop, Objetivo_1, Objetivo_2 FROM favoritos as f LEFT JOIN acciones as a on f.name = a.Ticker')
        db.conectar_sqlite(
            'INSERT OR IGNORE INTO new_fav SELECT * FROM new_fav_2')
        db.conectar_sqlite(
            'INSERT OR IGNORE INTO new_fav SELECT id, Fecha, País, Nombre, name, Soporte_Stop, Objetivo_1, Objetivo_2 FROM favoritos as f LEFT JOIN acciones as a on f.name = a.Ticker')
        listado_favs = db.consultarConSQL(
            'SELECT * FROM new_fav')
        contar_favs = db.consultarConSQL(
            'SELECT COUNT(name) FROM new_fav')
        for i in contar_favs:
            contar_fav = i['COUNT(name)']
        rentab = request.args.get('rentabilidad_final', "Ver rentabilidad")
        name_rent = request.args.get('name_rent')
        return render_template("favoritos.html", favoritos=listado_favs, contar=contar_fav, rentab=rentab, name_rent=name_rent, email=email)
    else:
        return redirect(url_for("index", email=email))


@app.route('/rentabilidad', methods=['GET', 'POST'])
def rent_favoritos():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        pais_rent = request.args.get('pais_rent')
        name_rent = request.args.get('name_rent')
        fecha_rent = request.args.get('fecha_rent')
        if pais_rent == "ESTADOS":
            pais_rent = "UNITED STATES"
        if pais_rent == "REINO":
            pais_rent = "REINO UNIDO"
        if pais_rent == "HOLAND":
            pais_rent = "NETHERLANDS"
        if fecha_rent != hoy:
            df = investpy.get_stock_historical_data(stock=name_rent,
                                                    country=GoogleTranslator(
                                                        source='auto', target='en').translate(pais_rent),
                                                    from_date=fecha_rent,
                                                    to_date=hoy)
            valor_final = df['Close'][len(df)-1]
            valor_inicial = df['Close'][0]
            rentabilidad = (((valor_final-valor_inicial) /
                            valor_inicial)*100).round(2)
            rentabilidad_final = str(rentabilidad).replace('.', ',')
            return redirect(url_for("obtener_favoritos", rentabilidad_final=rentabilidad_final, name_rent=name_rent, email=email))

        else:
            flash(
                "Debes elegir una fecha anterior a hoy para calcular su rentabilidad.", "error")
            return redirect(url_for("obtener_favoritos", email=email))


@app.route('/api', methods=['GET', 'POST'])
def alpha():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        consulta = request.args.get('consultar')
        if consulta != "None":
            try:
                ts = TimeSeries(key=api_alpha, output_format='pandas')
                df_consulta, meta_data = ts.get_daily(consulta)
                df_consulta.columns = [['Apertura', 'Máximo',
                                        'Mínimo', 'Cierre', 'Volumen']]
                df_consulta = df_consulta.head(20)
                df_consulta['Apertura'] = df_consulta['Apertura'].round(2)
                df_consulta['Máximo'] = df_consulta['Máximo'].round(2)
                df_consulta['Mínimo'] = df_consulta['Mínimo'].round(2)
                df_consulta['Cierre'] = df_consulta['Cierre'].round(2)
                df_consulta['Volumen'] = df_consulta['Volumen'].astype(int)
                df_consulta.index = df_consulta.index.strftime('%d/%m/%Y')
                consulta_ = consulta.upper()
                grafico = consulta_+'.png'
                return render_template("consulta.html", grafico=grafico, hist=[df_consulta.to_html(classes='data', col_space=10, justify='center', decimal=',', index_names=False)], email=email, consulta=consulta_)

            except ValueError:
                flash("No disponemos de tabla de históricos para esta acción.", "error")
            consulta_ = consulta.upper()
            grafico = consulta_+'.png'
            return render_template("consulta.html", grafico=grafico, email=email, consulta=consulta_)
        else:
            flash("Debes elegir un valor real para ver su histórico", "error")
            return redirect(url_for("listado_contenido", email=email))


@app.route('/salir')
def salir():
    email = request.args.get('email')
    usuario_clave = comprobar_usuario_clave()
    if usuario_clave == True:
        db.conectar_sqlite(
                    'UPDATE users SET clave = "0" WHERE user_email ="{}"'.format(email))
        session.clear()
        flash("Has salido de la sesión correctamente.", "exito")
    else:
        return redirect(url_for("index"))
    return render_template("index.html")
