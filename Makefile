populate_database_1:
	python -c 'from icook.recipe_database.database_handling import lowest_non_existant_id, new_db_entry_from_spoon_id; id = lowest_non_existant_id(); new_db_entry_from_spoon_id(id)'

populate_database_50:
	python -c 'from icook.recipe_database.database_handling import automated_db_population; automated_db_population(50)'
