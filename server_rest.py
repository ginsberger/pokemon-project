from flask import Flask,Response, request
from pymysql import IntegrityError
import json
import requests
from models import pokemon,type,trainer
import pokemon_api

app = Flask(__name__)


@app.route('/types/<pokemon_name>', methods=["PATCH"])
def update_type(pokemon_name):
    try:
        pokemon_data = pokemon_api.get_pokemon_by_name(pokemon_name)
    except Exception as e:
        return Response(json.dumps({"Error": "Not Found"}), 404)

    try:
        for type_ in pokemon_data["types"]:
            type.insert_type(type_)
            type_id = type.get_type_id(type_['type']['name'])
            pokemon_id = pokemon.get_pokemon_id(pokemon_name)
            pokemon.add_type(pokemon_id["id"], type_id["id"])

    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)
    
    return Response(json.dumps({"Success": "update types"}), 200)


@app.route('/pokemons', methods=["POST"])
def add_pokemon():
    pokemon_data = request.get_json()
    pokemon_fields = ["id", "name", "height", "weight", "types"]
    missing_fields = [x for x in pokemon_fields if not pokemon_data.get(x)]
    if missing_fields:
        return Response(json.dumps({"Error": f'fields {missing_fields} are missing'}), 400)

    try:
        pokemon.add_new_pokemon(pokemon_data["id"], pokemon_data["name"], pokemon_data["height"], pokemon_data["weight"], pokemon_data["types"]) 
        # for type_ in pokemon_data["types"]:
        #     type.insert_type(type_)
        #     type_id  = type.get_type_id(type_)
        #     type.add_type_to_pokemon(pokemon_data["id"], type_id["id"])

    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)
    
    return Response(json.dumps({"Success": "add pokemon"}), 200)


@app.route('/pokemons/<type_name>')
def pokemons_by_type(type_name):
    try:
        pokemons = type.get_pokemon_by_type(type_name)
        if not pokemons:
            return Response(json.dumps({"Error": f"Type  {type_name} does not exists"}), 404)

        return Response(json.dumps({"Pokemons": [pokemon["name_"] for pokemon in pokemons]}))

    except Exception as ex: 
        return Response(json.dumps({"Error": str(ex)}), 500)


@app.route('/pokemons/<trainer_name>')
def pokemons_by_trainer(trainer_name):
    try:
        pokemons = trainer.get_pokemons_by_trainer(trainer_name)
        if pokemons:    
            return Response(json.dumps({f"pokemons's {trainer_name}": [pokemon["name_"] for pokemon in pokemons] }),200)
        else:    
            return Response(json.dumps({"Error": "Not Found"}), 404)  

    except Exception as e:
            return Response(json.dumps({"Error": str(e)}), 500)


@app.route('/trainers/<pokemon_name>', methods=["GET"])
def find_owners(pokemon_name):
    try:
        trainers = pokemon.get_trainer_by_pokemon_name(pokemon_name)
        if trainers:    
            return Response(json.dumps({f"trainer's {pokemon_name}": [trainer["trainer_name"] for trainer in trainers]}), 200)
        else:    
            return Response(json.dumps({"Error": "Not Found"}), 404)
            
    except Exception as e: 
        return Response(json.dumps({"Error": str(e)}), 500) 


@app.route('/evolve/<pokemon_name>/<trainer_name>',methods=["PATCH"])
def evolve(pokemon_name, trainer_name):
    try:
        result = pokemon.check_owned_by(pokemon_name, trainer_name)
        if not result:
            return Response(json.dumps({"Error": "Not Found"}), 404)

        evolve = pokemon_api.get_next_in_evolution_chain(pokemon_name)
        if not evolve:
            return Response(json.dumps({"Error": f"Pokemon {pokemon_name} can not evolve"}), 403)

        pokemon_data = pokemon_api.get_pokemon_by_name(pokemon_name)
        pokemon.add_new_pokemon(pokemon_data["id"], evolve, pokemon_data["height"], pokemon_data["weight"], pokemon_data["types"])
        pokemon.update_pokemon_of_trainer(pokemon_name, evolve, trainer_name)

    except IntegrityError as error: 
        return Response(json.dumps({"Error": f"Trainer {trainer_name} already trained the evolve {evolve} pokemon"}), 409) 
        
    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)

    return Response(json.dumps({"Success": f"Pokemon {pokemon} evolved to {evolve} pokemon"}), 200)     


@app.route('/<pokemon_name>/<trainer_name>', methods=["DELETE"])
def delete_pokemon(pokemon_name, trainer_name):
    try:
        result = pokemon.check_owned_by(pokemon_name, trainer_name)
        if not result:
            return Response(json.dumps({"Error": f"Trainer {trainer_name} does not trained pokemon {pokemon_name}"}), 404)

        pokemon.delete_pokemon_of_trainer(pokemon_name, trainer_name)

    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)

    return Response(json.dumps({"Success": "delete pokemon"}), 200)


if __name__ == '__main__':
    app.run(port=3000)