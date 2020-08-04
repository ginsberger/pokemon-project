import pymysql
from pymysql import IntegrityError
import json


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="GgBb123!@#",
    db="pokemon_project",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def create_tables():
    with open("poke_data.json") as json_file:
        data = json.load(json_file)
        
    type_counter = 1

    for row in data:
        try:
            with connection.cursor() as cursor:
                try:
                    query = "INSERT into Type_ (id, type_name) values ({}, '{}')".format(type_counter, row["type"])
                    cursor.execute(query)
                    type_counter += 1
                except IntegrityError as error: 
                    pass # It's OK just except it 

                try:
                    query = "INSERT into Pokemon (id, name_, height, weight_) values ({}, '{}', {}, {})".format(row["id"], row["name"], row["height"], row["weight"])
                    cursor.execute(query)
                except IntegrityError as error: 
                    print( "Error: Pokemon already exists")
                
                try:
                    query = "SELECT id FROM Type_ WHERE type_name = '{}'".format(row["type"])
                    cursor.execute(query)
                    type = cursor.fetchone()

                    query = "INSERT into Pokemon_Type (type_id, pokemon_id) values ({}, {})".format(type["id"], row["id"])
                    cursor.execute(query)
                except IntegrityError as error: 
                    pass # It's OK just except it  
                
                for trainer in row["ownedBy"]:
                    try:
                        query = "INSERT into Trainer (name_, town) values ('{}', '{}')".format(trainer["name"], trainer["town"])
                        cursor.execute(query)
                    except IntegrityError as error: 
                        pass # It's OK just except it 

                    try:
                        query = "INSERT into OwnedBy (pokemon_id, pokemon_name, trainer_name) values ({}, '{}', '{}')".format(row["id"], row["name"], trainer["name"])
                        cursor.execute(query)
                    except IntegrityError as error: 
                        print( f'Error Trainer {trainer_name} already train pokemon {row["id"]}')              
                connection.commit()
        except Exception as ex:
            print (f"Error {str(ex)}")

create_tables()

