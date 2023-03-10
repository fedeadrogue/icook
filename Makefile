populate_database:
	python -c 'from icook.recipe_database.database_handling import lowest_non_existant_id, new_db_entry_from_spoon_id; id = lowest_non_existant_id(); new_db_entry_from_spoon_id(id)'
