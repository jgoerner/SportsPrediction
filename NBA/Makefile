armageddon:
	@python src/_clear_graph.py

graph: armageddon
	@python src/_create_arena_city_state_country.py
	@python src/_create_team_division_conference.py
	@python src/_connect_team_arena.py
	@python src/_create_game.py

    
data:
	@python src/_combine_season_data.py
    
all: data graph