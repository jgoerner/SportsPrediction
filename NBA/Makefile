data:
	@python src/_fetch_data_from_s3.py

armageddon:
	@python src/_clear_graph.py

graph: data armageddon
	@python src/_create_player.py
	@python src/_create_arena_city_state_country.py
	@python src/_create_team_division_conference.py
	@python src/_connect_team_arena.py
	@python src/_create_game.py
	@python src/_create_play_by_play.py

msf:
	@python src/_generate_msf_season_file.py
	@python src/_generate_msf_player_file.py
	@python src/_generate_msf_play_by_play_file.py