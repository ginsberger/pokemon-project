from pymysql import IntegrityError
import pymysql
from . import type

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="151428",
    db="pokemon_project",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def get_pokemon_id(pokemon_name):
    with connection.cursor() as cursor:
        query = "SELECT id FROM Pokemon WHERE name_ = '{}'".format(pokemon_name)
        cursor.execute(query)
        return cursor.fetchone()


def add_type(pokemon_id, type_id):
    with connection.cursor() as cursor:
        query = "INSERT into Pokemon_Type (type_id, pokemon_id) values ({}, {})".format(type_id, pokemon_id)
        try:
            cursor.execute(query)
            connection.commit()
        except IntegrityError as error: 
            pass # It's OK just except it 
        


def get_trainer_by_pokemon_name(pokemon_name):
    with connection.cursor() as cursor:
        query = "SELECT trainer_name FROM OwnedBy WHERE pokemon_name = '{}'".format(pokemon_name)
        cursor.execute(query)
        return cursor.fetchall()


def check_owned_by(pokemon_name, trainer_name):
    with connection.cursor() as cursor:
        query = "SELECT * FROM OwnedBy WHERE pokemon_name = '{}' and  trainer_name = '{}'".format(pokemon_name, trainer_name)
        cursor.execute(query)
        return cursor.fetchone()


def add_new_pokemon(pokemon_id, pokemon_name, pokemon_height, pokemon_weight, pokemon_types):
    with connection.cursor() as cursor:
        query = "INSERT into Pokemon (id, name_, height, weight_) values ({}, '{}', {}, {})".format(pokemon_id, pokemon_name, pokemon_height, pokemon_weight)
    try:    
        cursor.execute(query)
        for type_ in pokemon_types:
            type.insert_type(type_)
            type_id  = type.get_type_id(type_)
            type.add_type_to_pokemon(pokemon_id, type_id["id"])
        connection.commit() 
    except IntegrityError as error: 
        pass # It's OK just except it 


def update_pokemon_of_trainer(pre_evolve, evolve, trainer_name):
    with connection.cursor() as cursor:
        query = f"""UPDATE OwnedBy
                SET pokemon_name = '{evolve}'
                WHERE pokemon_name = '{pre_evolve}' and trainer_name = '{trainer_name}'"""
        cursor.execute(query)
        connection.commit() 


def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    with connection.cursor() as cursor:
        query = f"""DELETE FROM OwnedBy
                    WHERE pokemon_name = '{pokemon}' and trainer_name = '{trainer}'"""
        cursor.execute(query)
        connection.commit()
            