data:
	@python src/_fetch_data_from_s3.py
<<<<<<< HEAD
	@python src/_combine_season_data.py
=======
>>>>>>> 3ed6ea9d3c9087e71270069ecf81765a51f4859b

armageddon:
	@python src/_clear_graph.py

graph: data armageddon
	@python src/_create_arena_city_state_country.py
	@python src/_create_team_division_conference.py
	@python src/_connect_team_arena.py
	@python src/_create_game.py 