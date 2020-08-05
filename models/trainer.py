import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="151428",
    db="pokemon_project",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def get_pokemons_by_trainer(trainer_name):
    with connection.cursor() as cursor:
        query = '''SELECT P.name_ 
            FROM Pokemon P JOIN OwnedBy OB
            on P.id = OB.pokemon_id                 
            WHERE OB.trainer_name = "{}" '''.format(name)
        cursor.execute(query)
        return cursor.fetchall()