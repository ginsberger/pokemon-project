from flask import Flask,Response
import pymysql
from pymysql import IntegrityError
import json
import requests


app = Flask(__name__)


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="GgBb123!@#",
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


@app.route('/find_by_type/<type>')
def find_by_type(type):

    query = f"SELECT name_\
             FROM Pokemon P JOIN Type_ T JOIN Pokemon_Type PT \
             on PT.type_id = T.id and PT.pokemon_id = P.id\
             WHERE T.type_name = '{type}'"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            pokemons = cursor.fetchall()
            if not pokemons:
                return json.dumps({"Error": f"Type  {type} does not exists"}), 404
            return json.dumps({"Pokemons": [pokemon["name_"] for pokemon in pokemons]})

    except Exception as ex: 
        return {"Error": str(ex)}, 500   
    

@app.route('/evolve/<pokemon>/<trainer>')
def evolve(pokemon, trainer):

    # find evolve
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    pokemon_data = requests.get(url=pokemon_url,verify=False).json()
    species_url = pokemon_data["species"]["url"]
    species_info = requests.get(url=species_url,verify=False).json()
    evolution_chain_url = species_info["evolution_chain"]["url"]
    evolution_chain_info = requests.get(url=evolution_chain_url,verify=False).json()
    chain = evolution_chain_info["chain"]

    while chain["species"]["name"] != pokemon:
        chain = chain["evolves_to"][0]

    if len(chain["evolves_to"]) == 0:
        return Response(json.dumps({"Error": f"Pokemon {pokemon} can not evolve"}), 403)
    
    evolve = chain["evolves_to"][0]["species"]["name"]

    # update tables
    try:
        with connection.cursor() as cursor:
            query = "INSERT into Pokemon (id, name_, height, weight_) values ({}, '{}', {}, {})".format(pokemon_data["id"], evolve, pokemon_data["height"], pokemon_data["weight"])
            try:
                cursor.execute(query)
            except IntegrityError as error: 
                pass # It's OK just except it 

            query = f"""UPDATE OwnedBy
                    SET pokemon_name = '{evolve}'
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
            try:
                cursor.execute(query)
            except IntegrityError as error: 
                return Response(json.dumps({"Error": f"Trainer {trainer} already trained the evolve {evolve} pokemon"}), 400) #
        connection.commit() 
    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)

    return Response(json.dumps({"Success": f"Pokemon {pokemon} evolved to {evolve} pokemon"}), 200)    #    




if __name__ == '__main__':
    app.run(port=3000)

