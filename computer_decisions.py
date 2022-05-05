import numpy as np
import random

class Computer_RL():

	def __init__(self, exploration_decreasing_decay = 0.01, min_exploration_proba = 0.01, gamma = 0.99, lr = 0.1):
		self.exploration_proba = 1
		self.exploration_decreasing_decay = exploration_decreasing_decay
		self.min_exploration_proba = min_exploration_proba
		self.gamma = gamma
		self.lr = lr
		self.Q_table = np.zeros((2,2))
		self.decision_to_number = {
			"cooperate": 0,
			"defect": 1
		}
		self.number_to_decision = {
			0: "cooperate",
			1: "defect"
		}

		self.user_decision_sequence = []
		self.computer_decision_sequence = []
		self.points = 0
		self.round = 0


	def make_guess(self):
		if len(self.user_decision_sequence) > 0:
			current_state = self.user_decision_sequence[-1]
		else:
			current_state = 0

		if np.random.uniform(0,1) <= self.exploration_proba:
			action = random.randint(0, 1)
		else:
			action = int(np.argmax(self.Q_table[current_state,:]))
		self.computer_decision_sequence.append(action)
		return action

	def scale_reward(self, points):
		return (points - 1.) / 4.
	
	def update_state(self, state):
		if len(self.user_decision_sequence) > 0:
			prev_state = self.user_decision_sequence[-1]
			prev_action = self.computer_decision_sequence[-1]
			reward = self.scale_reward(state["computer_points"])
			self.Q_table[prev_state, prev_action] = (1-self.lr) * self.Q_table[prev_state, prev_action] + self.lr * (reward + self.gamma * max(self.Q_table[state["user_decision"],:]))
		self.round += 1
		self.user_decision_sequence.append(state["user_decision"])
		self.points += state["computer_points"]
		self.exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay*self.round))

class Computer_Random():
	def __init__(self):
		self.user_decision_sequence = []
		self.computer_decision_sequence = []
		self.points = 0
	
	def make_guess(self):
		action = random.randint(0, 1)
		self.computer_decision_sequence.append(action)
		return action
	
	def update_state(self, state):
		self.user_decision_sequence.append(state["user_decision"])
		self.points += state["computer_points"]

class Computer_Mimic():
	def __init__(self):
		self.user_decision_sequence = []
		self.computer_decision_sequence = []
		self.points = 0
	
	def make_guess(self):
		action = self.user_decision_sequence[-1] if len(self.user_decision_sequence) > 0 else random.randint(0,1)
		self.computer_decision_sequence.append(action)
		return action
	
	def update_state(self, state):
		self.user_decision_sequence.append(state["user_decision"])
		self.points += state["computer_points"]

		


