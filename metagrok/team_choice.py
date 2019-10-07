import random
import numpy as np

def teamchoice_random(team_list):
	return random.choice(range(len(team_list)))

def teamchoice_alwayszero(team_list):
	return 0

def random_profile(strategy_count :int):
	return random.choice(range(strategy_count))

class AgentStrategyProfile(object):
	def __init__(self, pure_strategy_count,opponent_strategy_count, strategy = None):
		#self.utility_function = np.zeros((pure_strategy_count, opponent_strategy_count))
		self.p1_strategy_count = pure_strategy_count
		self.p2_strategy_count = opponent_strategy_count
		self.utility_sum = np.zeros((pure_strategy_count, opponent_strategy_count))
		self.game_count = np.zeros((pure_strategy_count, opponent_strategy_count))
		if strategy == None:
			self.strategy = random_profile
		else:
			self.strategy = strategy

			
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
