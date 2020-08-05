
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
    
    return Response(json.dumps({"Success": "add pokemon"}), 200)
<<<<<<< HEAD
=======


# I added the Pokemon number 161 from  the api


@app.route('/delete_pokemon_of_trainer/<pokemon>/<trainer>', methods=["DELETE"])
def delete_pokemon(pokemon, trainer):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT *
                    FROM OwnedBy
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return Response(json.dumps({"Error": f"Trainer {trainer} does not trained pokemon {pokemon}"}), 404)

            query = f"""DELETE FROM OwnedBy
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
            cursor.execute(query)
            connection.commit()
            
    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)

    return Response(json.dumps({"Success": "delete pokemon"}), 200)
>>>>>>> 7402a0c176f08bf9cf12e58570897a72b2b41d4c


@app.route('/delete_pokemon_of_trainer/<pokemon>/<trainer>', methods=["DELETE"])
def delete_pokemon(pokemon, trainer):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT *
                    FROM OwnedBy
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return Response(json.dumps({"Error": f"Trainer {trainer} does not trained pokemon {pokemon}"}), 404)

            query = f"""DELETE FROM OwnedBy
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
            cursor.execute(query)
            connection.commit()
            
    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), 500)

    return Response(json.dumps({"Success": "delete pokemon"}), 200)


if __name__ == '__main__':
    app.run(port=3000)