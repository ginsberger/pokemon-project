from flask import Flask,Response, request
import pymysql
from pymysql import IntegrityError
import json
import requests


app = Flask(__name__)


connection = pymysql.connect(
    host="localhost",
    user="RENT",
    password="",
    db="sql_pokemon",
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


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    pokemon_fields = ["id", "name", "height", "weight", "types"]
    missing_fields = [x for x in pokemon_fields if not pokemon.get(x)]
    if missing_fields:
        return Response(json.dumps({"Error": f'fields {missing_fields} are missing'}), 400)

    try:
        with connection.cursor() as cursor:

            query = "INSERT into Pokemon values({}, '{}', {}, {})".format(pokemon["id"],
                pokemon["name"],
                pokemon["height"],
                pokemon["weight"]
            )
            cursor.execute(query)

            for type in pokemon["types"]:
                query = "INSERT into Type_ values(NULL, '{}')".format(type)
                try:
                    cursor.execute(query)
                except IntegrityError as error: 
                    pass # It's OK just except it 

                query = "SELECT id FROM Type_ WHERE type_name = '{}'".format(type)
                cursor.execute(query)
                type_id = cursor.fetchone()

                query = "INSERT into Pokemon_Type values({}, {})".format(pokemon["id"], type_id["id"])
                try:
                    cursor.execute(query)
                except IntegrityError as error: 
                    pass # It's OK just except it 
            connection.commit()

    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)
    
    return Response(json.dumps({"Success": "update types"}), 200)


# I added the Pokemon number 161 from  the api

if __name__ == '__main__':
    app.run(port=3000)

# http://127.0.0.1:3000/add_pokemon
# {
#     "id": 161,
#     "name": "sentret",
#     "height": 8,
#     "weight": 60,
#     "types": ["normal"]
# }