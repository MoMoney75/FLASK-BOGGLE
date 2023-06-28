
from flask import Flask
from flask import render_template, session, request, jsonify
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
boggle_game = Boggle()
board = boggle_game.make_board()

"""shows home page"""
@app.route('/')
def show_board():
    """creates a gameboard from make_board function,adds the
    gameboard to session"""
    board = boggle_game.make_board()
    session['board'] = board

    """using session, keep track of the highest score
    and number of times played"""
    highScore = session.get('highScore', 0)
    numplays = session.get("numplays", 0)

    return render_template("base.html", board=board, highScore=highScore, numplays=numplays)


"""when a word is submitted, checked to see if word is valid and
returns a response"""
@app.route('/answer', methods=['GET'])
def handle_answer():
    word = request.args['word']
    board = session['board']
    response_string = boggle_game.check_valid_word(board, word)

    return jsonify({'response': response_string})


@app.route('/end-game', methods=['POST'])
def endGame():
    score = request.json['score']

    highScore = session.get('highScore', 0)
    numplays = session.get('numplays', 0)


    """when clock runs out, gets the current score and compares to
    the previous high score to determine if a new high score"""
    session['highScore'] = max(score, highScore)

    """gets current number of times played from session
    and increments by 1 at the end of each game"""
    session['numplays'] = numplays + 1

    return 'game over'
