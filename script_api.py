import os
import json
import pymysql
from flask import Flask, request, jsonify, abort
from sql_connection import *

# Vérification des variables d'environnement
print("MYSQL_HOST:", MYSQL_HOST)
print("MYSQL_USER:", MYSQL_USER)
print("MYSQL_PASSWORD:", MYSQL_PASSWORD)
print("MYSQL_DB:", MYSQL_DB)

app = Flask(__name__)

# Fonction pour établir une connexion à la base de données
def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

# Endpoint pour récupérer la liste des réponses du survey
@app.route("/survey", methods=["GET"])
def get_survey():
    db_conn = get_db_connection()
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM survey")
        results = cursor.fetchall()
    db_conn.close()
    return jsonify(results)

# Endpoint pour récupérer une réponse spécifique du survey par ID
@app.route("/survey/<int:id>", methods=["GET"])
def get_survey_by_id(id):
    db_conn = get_db_connection()
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM survey WHERE `index`=%s", (id,))
        result = cursor.fetchone()
        if not result:
            abort(404)
    db_conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5002)

