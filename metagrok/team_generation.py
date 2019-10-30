from metagrok import team_definition as p
import random


def generate_random_pokemon(species=None,level=100):
	if species == None:
		species = random.choice(p.pokemon_names)
	item = random.choice(p.items)
	ability = random.choice([p.pokemon[species]["abilities"][x] for x in p.pokemon[species]["abilities"].keys()])
	moves = random.sample(p.learnsets[species]["legal_moves"], min(4, len(p.learnsets[species]["legal_moves"])))
	nature = random.choice(p.natures)
	ivs = [31] * 6 #TODO: There are situations in which this might not be optimal...
	level = level
	pts_allocated = 0
	evs = [0] * 6
	while pts_allocated < 508:
		possible_stats_to_add_evs = []
		for i in range(6):
			if not evs[i] >= 252:
				possible_stats_to_add_evs.append(i)
		evs[random.choice(possible_stats_to_add_evs)] += 4
		pts_allocated += 4
	return p.Pokemon(species, item,ability, moves, nature,evs, ivs, level)

def generate_random_team():
	team = []
	for i in range(0, 6):
		team.append(generate_random_pokemon())
	for pokemon in team:
		print(pokemon.export_to_line())

def get_legal_pokemon(tier):
	legal_pokemon = []
	for pokemon in p.pokemon:
		if p.metagame_legalities.get(pokemon, None) != None:
			if p.metagame_legalities[pokemon]["tier"] == tier:
				legal_pokemon.append(pokemon)
	return legal_pokemon


def generate_random_monotype_lc_team(type):
	team = []
	legal_pokemon = get_legal_pokemon("LC")
	legal_in_type = []
	for pokemon in legal_pokemon:
		if type in p.pokemon[pokemon]["types"]:
			legal_in_type.append(pokemon)
	if len(legal_in_type) < 6:
		print("less than 6 pokemon in type, you wont have a team")
		raise(Exception)
	else:
		chosen_pokemon = random.sample(legal_in_type, 6)
		for pokemon in chosen_pokemon:
			team.append(generate_random_pokemon(species=pokemon, level=5))
		for pokemon in team:
			print(pokemon.export_to_line())
	return "]".join([pokemon.export_to_line() for pokemon in team])


def init_lc_thunderdome():
	print("welcome to the thunderdome for babies")
	print("n babies enter, one baby leaves")
	p1_teams = [generate_random_monotype_lc_team("Water")]
	p2_teams = [generate_random_monotype_lc_team("Fire") for i in range(0, 5)]
	p2_teams.append(generate_random_monotype_lc_team("Ground"))
	p2_teams.append(generate_random_monotype_lc_team("Electric"))
	return p1_teams, p2_teams


print(len(get_legal_pokemon("LC")))
generate_random_monotype_lc_team("Fire")


#generate_random_team()
