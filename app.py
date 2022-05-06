from flask import Flask, redirect, request, render_template, session
from game import Game

app = Flask(__name__)
app.secret_key = '\x99\xcd\x94\xe6\xc6\xf2\xcb`O\xbd\xd6\r'


@app.route("/", methods = ["GET", "POST"])
def index():
	if request.method == "POST":
		computer_option = request.form.get("options")
		return redirect(f"/play?computer_option={computer_option}")
	return render_template("index.html")

@app.route("/play", methods = ["GET", "POST"])
def play():

	if request.method == "GET":

		computer_option = request.args.get('computer_option', default = "RANDOM", type = str)
		game_ = Game(mode = computer_option)
		session["game"] = game_.serialize()
		return render_template("play.html", game_state = game_.package_state())

	if request.method == "POST":

		player_choice_number = request.form.get("user_choice").strip()

		game_ = Game.restore_session(session["game"])

		if player_choice_number not in ["0", "1"]:
			return render_template("play.html", game_state = game_.package_state())

		game_.advance_state(player_choice_number.strip())
		session["game"] = game_.serialize()
		if game_.game_end:
			return redirect("/finished")
		return render_template("play.html", game_state = game_.package_state())

@app.route("/finished", methods = ["GET"])
def finished():
	game_ = Game.restore_session(session["game"])
	return render_template("finished.html", game_state = game_.package_state())

if __name__ == "__main__":
	app.run(debug = True)