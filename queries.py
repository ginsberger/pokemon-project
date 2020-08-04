from flask import Flask,Response
import pymysql
from pymysql import IntegrityError
import json
import requests


app = Flask(__name__)


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="151428",
    db="pokemon_project",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/update_type/<name>', methods=["PATCH"])
def update_type(name):
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    types_name = requests.get(url=pokemon_url,verify=False).json()
    if types_name.get("types"):
        try:
            with connection.cursor() as cursor:
                for type in types_name["types"]:
                    query = "INSERT into Type_ (id, type_name) values (NULL, '{}')".format(type['type']['name'])
                    try:
                        cursor.execute(query)
                    except IntegrityError as error: 
                        pass # It's OK just except it 

                    try:
                        query = "SELECT id FROM Type_ WHERE type_name = '{}'".format(type['type']['name'])
                        cursor.execute(query)
                        type_id = cursor.fetchone()
                        
                        query = "SELECT id FROM Pokemon WHERE name_ = '{}'".format(name)
                        cursor.execute(query)
                        pokemon_id = cursor.fetchone()
                        
                        query = "INSERT into Pokemon_Type (type_id, pokemon_id) values ({}, {})".format(type_id["id"], pokemon_id["id"])
                        cursor.execute(query)
                    except IntegrityError as error: 
                        pass # It's OK just except it 
                    connection.commit()    
        except Exception as e:
            return Response(json.dumps({"Error": str(e)}), 500)

    else:
        return Response(json.dumps({"Error": "Not Found"}), 404)

    return Response(json.dumps({"Success": "update types"}), 200)


@app.route('/get_trainers/<name>', methods=["GET"])
def find_owners(name):

    query = "SELECT trainer_name FROM OwnedBy WHERE pokemon_name = '{}'".format(name)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            trainers = cursor.fetchall()
            return Response(json.dumps({f"trainer's {name}": [trainer["trainer_name"] for trainer in trainers]}), 200)
    except Exception as e: 
        return Response(json.dumps({"Error": str(e)}), 500) 


if __name__ == '__main__':
    app.run(port=3000)

