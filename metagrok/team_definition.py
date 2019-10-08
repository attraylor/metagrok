import json

pokemon = json.load(open("dex/BattlePokedex.json")).keys()
items = json.load(open("dex/BattleItems.json")).keys()
abilities = json.load(open("dex/BattleAbilities.json")).keys()
all_moves = json.load(open("dex/BattleMovedex.json")).keys()
learnsets = json.load(open("dex/BattleLearnsets.json"))

natures = ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", \
           "Gentle", "Hardy", "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", \
		   "Modest", "Naive", "Naughty", "Quiet", "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]


def clean(s):
	return s.replace(" ", "").replace("-", "").replace("[", "").replace("]", "").lower()

class Pokemon(object):
	def __init__(self, species : str, item : str,
				 ability : str, moves : list, nature : str = "Serious",
				 ev_arr : str = [0,0,0,0,0,0], iv_arr : list = [31,31,31,31,31,31], level : int = 100):
		self.species = clean(species)
		self.item = clean(item)
		self.ability = clean(ability)
		self.moves = [clean(move) for move in moves]
		self.nature = nature
		self.ev_arr = ev_arr
		self.iv_arr = iv_arr
		self.level = level
		self.check_if_legal()

	def check_if_legal(self):
		assert self.species in pokemon
		assert self.item in items
		assert self.ability in abilities
		assert self.nature in natures
		assert len(self.moves) > 0 and len(self.moves) < 5
		for move in self.moves:
			assert move in learnsets[self.species]["learnset"].keys() and \
				any(["7" in learn_type for learn_type in learnsets[self.species]["learnset"][move]])
		assert len(self.ev_arr) == 6
		assert sum(self.ev_arr) < 511 #len...
		for i in range(0, 6):
			assert self.ev_arr[i] < 256
		for i in range(0, 6):
			assert self.iv_arr[i] >= 0 and self.iv_arr[i] < 32
		assert self.level > 0 and self.level <= 100
		return True


	def export_to_line(self):
		ev_arr_print = ",".join([str(i) if i > 0 else "" for i in self.ev_arr])
		moves_print = ",".join(self.moves)
		iv_arr_print = ",".join([str(i) if i > 0 else "" for i in self.iv_arr])
		return "{}||{}|{}|{}|{}|{}||{}|{}|".format(self.species,self.item, self.ability, moves_print, self.nature,ev_arr_print,iv_arr_print,self.level)
