from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}.
    
    
    """ 

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game


    return jsonify({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """Listens for post requests and extracts a JSON object with game-id & word entry. 
    Will check if word is valid in the word list and findable on the board.
    Returns a JSON response with validity."""
                                  
    game_id = request.json["game_id"]
    word = request.json["word"]
    
    game = games[game_id]
    word_is_word = game.is_word_in_word_list(word) 
    word_on_board = game.check_word_on_board(word) 

    if not word_is_word:
        return jsonify({"result": "not-word"})

    if not word_on_board:
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})

