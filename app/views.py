__author__ = 'afordyce'


import flask
import uuid

from app import app, models


game_tracker = {}


@app.route('/')
@app.route('/index')
def index():
    data = {'message': 'Hello world!'}
    return flask.jsonify(**data)


@app.route('/paper-rock-scissors/<client_name>/')
def start_game(client_name):
    game_key = uuid.uuid4()
    url = flask.url_for('shoot', client_name=client_name, game_key=game_key)
    data = {"url": url}
    if client_name == 'Wang_Xu_Zhou':
        bot = models.WangXuZhou(None, None, None)
    elif client_name == 'Anti_Wang_Xu_Zhou':
        bot = models.AntiWangXuZhou(None, None, None)
    elif client_name == 'Weighted_Bot':
        bot = models.WeightedBot(None, None, None)
    elif client_name == 'Awesome_Bot':
        bot = models.AwesomeBot(None, None, None)
    else:
        bot = models.RPS_Basic(None, None, None)
    game_tracker[str(game_key)] = bot
    return flask.jsonify(**data)


@app.route('/paper-rock-scissors/<client_name>/<game_key>/')
def shoot(client_name, game_key):
    my_prev = flask.request.args.get('yourPreviousAction', None)
    opp_prev = flask.request.args.get('opponentPreviousAction', None)
    prev_outcome = flask.request.args.get('outcome', None)
    bot = game_tracker[game_key]
    bot.last_result = prev_outcome
    bot.my_prev = my_prev
    bot.opp_prev = opp_prev
    action = bot.get_next_action()
    data = {"action": action}
    return flask.jsonify(**data)
