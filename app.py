import streamlit as st

from game import Game

mode = st.radio(
	"Computer Mode",
	options = ["RL", "Random", "Mimic"]
)
if type(mode) == str:
	start = st.button("Start Game")
	if start:
		new_game = Game(mode = mode)
