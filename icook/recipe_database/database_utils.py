import numpy as np
import matplotlib.pyplot as plt
import cv2
import sqlite3
import time
from icook.recipe_database.database_handling import lowest_non_existant_id, new_db_entry_from_spoon_id

recipe_database = 'recipe_sqlite.db'

def show_image_from_db(id, recipe_database:str=recipe_database):
    '''Retrieve image by id, convert from blob format and show'''

    sqliteConnection = sqlite3.connect(recipe_database)
    cursor = sqliteConnection.cursor()

    image_query = f"""
    SELECT image
    FROM recipes
    WHERE recipe_id = {id}
    """
    query_result = cursor.execute(image_query)
    images = query_result.fetchall()

    sqliteConnection.close()

    nparr  = np.frombuffer(images[0][0], np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    plt.imshow(img_np)
