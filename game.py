import numpy as np
from computer_decisions import *

class Game():

	def __init__(self, mode: str = None, to_restore: bool = False):
		if not to_restore:
			self.mode = mode
			if self.mode == "RL":
				self.computer = Computer_RL()
			if self.mode == "RANDOM":
				self.computer = Computer_Random()
			if self.mode == "MIMIC":
				self.computer = Computer_Mimic()

			self.number_to_decision = {
				"0": "cooperate",
				"1": "defect"
			}
			
			self.states = []
			self.user_points = 0
			self.computer_points = 0
			self.round_number = 0
			self.total_rounds = random.randint(5, 15)
			self.game_end = False
			self.winner = ""

	def serialize(self):
		self.__dict__["computer"] = self.computer.__dict__
		return self.__dict__

	def restore_session(d: dict):
		new_game = Game(to_restore=True)
		for k in d.keys():
			if k == "computer":
				if d["mode"] == "RL":
					comp = Computer_RL
				if d["mode"] == "RANDOM":
					comp = Computer_Random
				if d["mode"] == "MIMIC":
					comp = Computer_Mimic
				new_game.__dict__[k] = comp.restore_session(d["computer"])
			else:
				new_game.__dict__[k] = d[k]
		return new_game
		
	
	def advance_state(self, user_input):
		user_guess = int(user_input.strip())
		computer_guess = self.computer.make_guess()
		state = {
			"user_decision": user_guess,
			"computer_decision": computer_guess
		}
		user_points, computer_points = self.calculate_points(user_guess, computer_guess)
		state["user_points"] = user_points
		state["computer_points"] = computer_points
		self.user_points += user_points
		self.computer_points += computer_points

		self.computer.update_state(state)
		self.states.append(state)
		self.round_number += 1
		if self.round_number >= self.total_rounds:
			self.game_end = True
			self.find_winner()
	
	def find_winner(self):
		if self.user_points > self.computer_points:
			self.winner = "User"
		elif self.user_points < self.computer_points:
			self.winner = "Computer"
		elif self.user_points == self.computer_points:
			self.winner = "Tie"

	
	def calculate_points(self, user_guess, computer_guess):
		if user_guess == computer_guess == 0:
			return (3., 3.)
		
		if user_guess == computer_guess == 1:
			return (1., 1.)
		
		if (user_guess == 1) and (computer_guess == 0):
			return (5., 0.)
		
		if (user_guess == 0) and (computer_guess == 1):
			return (0., 5.)
		
		return (0., 0.)

	
	def print_state(self):
		print("------------------------------------------")
		print("Game State:")
		if len(self.states) > 0:
			print("------------------------------------------")
			print()
			print(f"User's choice: {self.number_to_decision[str(self.states[-1]['user_decision'])]}")
			print(f"Computer's choice: {self.number_to_decision[str(self.states[-1]['computer_decision'])]}")
			print()
			print(f"User awarded {self.states[-1]['user_points']} points")
			print(f"Computer awarded {self.states[-1]['computer_points']} points")
			print()
		print("------------------------------------------")
		print()
		print(f"Total User Points: {self.user_points}")
		print()
		print(f"Total Computer Points: {self.computer_points}")
		print()
		print("------------------------------------------")
	
	def package_state(self):
		return {
			"round_number": self.round_number,
			"total_rounds": self.total_rounds,
			"user_points": self.user_points,
			"computer_points": self.computer_points,
			"prev_user_choice": self.number_to_decision[str(self.states[-1]['user_decision'])] if len(self.states) > 0 else None,
			"prev_computer_choice": self.number_to_decision[str(self.states[-1]["computer_decision"])] if len(self.states) > 0 else None,
			"prev_user_reward": self.states[-1]['user_points'] if len(self.states) > 0 else None,
			"prev_computer_reward": self.states[-1]['computer_points'] if len(self.states) > 0 else None,
			"winner": self.winner
		}
		