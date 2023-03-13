import sqlite3
import streamlit as st

# Create a connection to the database
conn = sqlite3.connect('recipe_sqlite.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    # Create the recipes table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_recipes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            recipes_id STRING NOT NULL
        );
    ''')
    conn.commit()

def add_recipe(user_id, recipes_list):
    # Insert a new recipe into the recipes table
    c.execute('''
        INSERT INTO user_recipes (user_id, recipes_id)
        VALUES (?, ?)
    ''', (user_id, recipes_list))
    conn.commit()

def get_recipes(id):
    # Get all recipes for a given user
    id = str(id)
    c.execute(f"SELECT recipes_id FROM user_recipes WHERE user_id='{id}'")
    recipes = c.fetchall()
    return recipes

if __name__ == '__main__':
    pass
