from game import Game

def main():
	print("Welcome to Prisoner's Dilemma!")
	computer_mode = ""
	while computer_mode not in ["RL", "RANDOM", "MIMIC"]:
		computer_mode = input("What computer mode would you like to play against? (rl/random/mimic)").upper()
	new_game = Game(mode = computer_mode)

	new_game.print_state()

	user_input = ""

	while not new_game.game_end:
		user_input = input("Please make your choice (0: cooperate, 1: defect, q: quit)").strip()

		while user_input not in ["0", "1", "q"]:
			user_input = input("Please make your choice (0: cooperate, 1: defect, q: quit)").strip()

		if user_input == "q":
			break
			
		new_game.advance_state(user_input.strip())

		new_game.print_state()

	if new_game.winner == "Tie":
		print("The result was a tie!!!")
	else:
		print(f"The winner is ... {new_game.winner}!!!")

if __name__ == "__main__":
	main()
			
		
		
