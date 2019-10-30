import random
import numpy as np

def teamchoice_random(team_list):
	return random.choice(range(len(team_list)))

def teamchoice_alwayszero(team_list):
	return 0

def random_profile(strategy_count :int):
	return random.choice(range(strategy_count))

class AgentStrategyProfile(object):
	def __init__(self, teams_player, teams_opponent, strategy = None, metagame = "gen7lc"):
		#self.utility_function = np.zeros((pure_strategy_count, opponent_strategy_count))
		self.p1_teams = teams_player
		self.p2_teams = teams_opponent
		self.metagame = metagame
		self.p1_strategy_count = len(self.p1_teams)
		self.p2_strategy_count = len(self.p2_teams)
		self.utility_sum = np.zeros((self.p1_strategy_count, self.p2_strategy_count))
		self.game_count = np.zeros((self.p1_strategy_count, self.p2_strategy_count))
		if strategy == None:
			self.strategy = random_profile
		else:
			self.strategy = strategy

	def get_teams(self,p1_ind, p2_ind):
	  #Used for initial team matchup experiments.
	  team_1 = self.p1_teams[p1_ind]
	  team_2 = self.p2_teams[p2_ind]
	  return dict(
	        formatid=self.metagame,
	        p1= {'name': 'p1', 'team': team_1},
	        p2 = {'name': 'p2', 'team': team_2},
	    )

	def update(self, p1_strategy_index: int, p2_strategy_index:int, p1_win : bool):
		self.game_count[p1_strategy_index][p2_strategy_index] += 1
		if p1_win == True:
			self.utility_sum[p1_strategy_index][p2_strategy_index] += 1
		else:
			self.utility_sum[p1_strategy_index][p2_strategy_index] -= 1

	def expected_utility(self, p1_strategy_index:int, p2_strategy_index:int):
		return self.utility_sum[p1_strategy_index][p2_strategy_index] / max(1e-10, self.game_count[p1_strategy_index][p2_strategy_index])

	def select_action(self):
		return self.strategy(self.p1_strategy_count)

	#MAY BE DEPRECATED BASED ON EVALUATION?
	def select_action_p2(self):
		return self.strategy(self.p2_strategy_count)

	def get_utility_matrix(self):
		return np.nan_to_num(self.utility_sum / self.game_count)
