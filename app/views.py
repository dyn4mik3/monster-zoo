from flask import render_template, flash, redirect, session, url_for, request, get_flashed_messages, g
from flask.ext.security import login_required
from flask.ext.security.forms import LoginForm, RegisterForm
from flask.ext.socketio import send, emit, join_room
import uuid

from app import app, socketio, db
from models import Gameroom
from engine import Game, Player


# Helper Functions

def check_for_live_gameroom(game_id):
    if Gameroom.query.get(game_id):
        return True
    else:
        return False

# URL Routes

@app.route('/')
def index():
    """
    Homepage - Displays marketing content and active games/users.
    """
    return render_template('index.html', login_user_form=LoginForm(), register_user_form=RegisterForm())

@app.route('/solo-room')
def solo_room():
    """
    Solo game vs AI.
    """
    return render_template('solo_room.html')

@app.route('/room/<int:game_id>')
def game_room(game_id):
    if check_for_live_gameroom(game_id):
        return render_template('multiplayer_room.html', game_id=game_id)
    else:
        return render_template('404.html'), 404

@app.route('/host')
@login_required
def host_game():
    """
    Create a game room, send user to the room URL.
    """
    game = Gameroom()
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('game_room', game_id=game.id))

@app.route('/lobby')
def lobby():
    """
    Load lobby page, user will enter in room ID and then be redirected to room URL.
    """
    return render_template('lobby.html')

@app.route('/join-game-room', methods=['POST'])
def join_game_room():
    """
    Check to see if game is in database. If so, redirect to room. If not, send back to lobby.
    """
    game_id = request.form['game-id']
    if check_for_live_gameroom(game_id):
        return redirect(url_for('game_room', game_id=game_id))
    else:
        flash('Bad Game ID: %s.' % game_id)
        flash('Please Try Again.')
        return render_template('lobby.html')

# Routes for static content / static templates

@app.route('/cards')
def cards():
    return render_template('content/cards.html')

@app.route('/story')
def story():
    return render_template('content/story.html')

@app.route('/art')
def art():
    return render_template('content/art.html')

@app.route('/game')
def game_info():
    return render_template('content/game.html')

@app.route('/printandplay')
def printandplay():
    return render_template('content/print_and_play.html')

@app.route('/about')
def about():
    return render_template('content/about.html')

@app.route('/rules')
def rules():
    return render_template('content/rules.html')

@app.route('/credits')
def credits():
    return render_template('content/credits.html')

"""
Socketio messaging.
"""
@socketio.on('connect', namespace='/game')
def connect():
    """
    Assigns a player_id and matching room to each connection. Stores the player_id in a session
    so we can use it later.
    """
    player_id = uuid.uuid4()
    session['player_id'] = player_id
    # put the player in a room for direct communication
    room = player_id
    join_room(room)
    emit('connected', {'player_id': player_id})
    emit('alert', 'Player connected to private room %s' % room, room=room)
    print 'SocketIO Connection Made (%s)' % session['player_id']

@socketio.on('disconnect', namespace='/game')
def disconnect():
    """
    Clean up after socket disconnects. Get rid of host game from Gamerooms table.
    """
    if 'host_game_id' in session:
        print 'Host game identified.'
        game_room = Gameroom.query.get(session['host_game_id'])
        if game_room:
            db.session.delete(game_room)
            print 'Removed Gameroom ID: %s from Gamerooms' % session['host_game_id']
    print 'SocketIO Disconnected (%s)' % session['player_id']


MAX_PLAYERS_IN_GAMEROOM = 2

live_games = {}

@socketio.on('game_connect', namespace='/game')
def game_connect(data):
    """
    User is on game page at this point. Add them to the socketio room. Add them as a player to the Game.
    """
    game_id = data['game_id']  # taken from the game page
    player_id = session['player_id']  # player_id is already stored in the socketio session on connect

    # Check to see if game room is valid
    if check_for_live_gameroom(game_id):
        # Check to see if game has been created. If not, create game.
        if game_id in live_games:
            game = live_games[game_id]
            print 'Game found for game_id %s' % game_id
        else:
            game = Game(game_id)
            live_games[game_id] = game
            print 'Game %s created for Gameroom %s' % (game, game_id)
        # Try to add player to game room.
        if game.add_player(player_id):
            join_room(game_id)
            emit('alert', 'Player %s has been added to game %s' % (player_id, game_id), room=game_id)
        else:
            print 'Player %s can not be added to game. Redirecting to lobby.' % player_id
            emit('redirect', {'url': url_for('lobby')}, room=player_id)
        if game.ready():
            print 'Game is ready. Starting.'
            print live_games
            game.start()
            emit('game_start', {'game_id': game.game_id}, room=game_id)

@socketio.on('get_game_state', namespace='/game')
def send_game_state(data):
    """
    Start game and send render signal with data
    :param data:
    :return:
    """
    player_id = session['player_id']
    game_id = data['game_id']
    try:
        game = live_games[game_id]
        emit('render_state', game.state.to_JSON(), room=game_id)
        print 'Sent render_state signal to clients'
    except:
        print 'Not a live game.'
        #emit('redirect', {'url': url_for('lobby')}, room=player_id)





