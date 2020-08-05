from pymysql import IntegrityError
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="151428",
    db="pokemon_project",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def insert_type(type_):
    with connection.cursor() as cursor:
        query = "INSERT into Type_ (id, type_name) values (NULL, '{}')".format(type_['type']['name'])
        try:
            cursor.execute(query)
            connection.commit()
        except IntegrityError as error: 
            pass # It's OK just except it 
        
        
def get_type_id(type_):
    with connection.cursor() as cursor:
        query = "SELECT id FROM Type_ WHERE type_name = '{}'".format(type_['type']['name'])
        cursor.execute(query)
        return cursor.fetchone()
                        
                        
def get_pokemon_by_type(type_):
    with connection.cursor() as cursor:
        query = f"""SELECT name_
            FROM Pokemon P JOIN Type_ T JOIN Pokemon_Type PT 
            on PT.type_id = T.id and PT.pokemon_id = P.id
            WHERE T.type_name = '{type_}'"""
        cursor.execute(query)
        return cursor.fetchall()


def add_type_to_pokemon(pokemon_id, type_id):
    with connection.cursor() as cursor:
        query = "INSERT into Pokemon_Type values({}, {})".format(pokemon_id, type_id)
        try:
            cursor.execute(query)
            connection.commit()
        except IntegrityError as error: 
            pass # It's OK just except it 
    