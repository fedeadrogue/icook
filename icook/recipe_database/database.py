import sqlite3
from icook.ml_logic.APIs import SpoonAPIcall

def create_database():
    '''Create an SQLite database in the local directory
    with the two tables recipes and steps'''

    file = 'recipe_sqlite.db'
    sqliteConnection = sqlite3.connect(file)
    cursor = sqliteConnection.cursor()

    table_recipes_query = '''
    CREATE TABLE IF NOT EXISTS recipes
    (
        [recipe_id] INTEGER PRIMARY KEY,
        [title] TEXT NOT NULL,
        [image] BLOB NOT NULL,
        [prep_time] INTEGER NOT NULL,
        [ingredients] TEXT NOT NULL,
        [source] TEXT NOT NULL,
        [source_url] TEXT NOT NULL
    )
    '''

    table_steps_query = '''
    CREATE TABLE IF NOT EXISTS steps
    (
        [step_id] TEXT PRIMARY KEY,
        [step_nr] BLOB NOT NULL,
        [step_description] INTEGER NOT NULL,
        [title] TEXT NOT NULL
    )
    '''

    cursor.execute(table_recipes_query)
    cursor.execute(table_steps_query)
    sqliteConnection.commit()
    sqliteConnection.close()

def populate_from_spoon(ingredient: str, number:int=10):
    pass


if __name__ == '__main__':
    create_database()
