from flask import Flask, render_template, request, current_app
import logging
import gevent.wsgi
import json

from vote import queue, redis_handler
from vote.signals import app_start

app = Flask(__name__, instance_path='/voting-machine/vote/web/')

TEAMS_COMPETING = []


def init_app(app):
    """
    Initialize the rabbitmq extension.
    """
    rabbit_queue = queue.Queue()
    r_handler = redis_handler.RedisHandler()

    app.extensions['rabbit_queue'] = rabbit_queue
    app.extensions['r_handler'] = r_handler


@app_start.connect
def start_extensions(app, **kwargs):
    """
    Start redis and rabbitmq at app startup
    """
    extensions = [
        app.extensions.get('rabbit_queue'),
        app.extensions.get('r_handler')
    ]

    for extension in extensions:
        if extension:
            extension.start()


def votes():
    """
    app route to show the results of voting

    :return: rendered template of the voting results
    """
    vote_total = {}
    for team in range(1, 5):
        team = 'team{}'.format(team)
        vote_total[team] = current_app.extensions['r_handler'].get_key(team)
        if vote_total[team] is None:
            vote_total[team] = 0

    return vote_total


@app.route('/', methods=['GET', 'POST'])
def place_vote():
    """
    Main page,
    :return: rendering a page with the status message of the vote for POST
    :return: rendering the default voting page for GET requests
    """
    vote_total = votes()
    if request.method == 'POST':
        team = request.form['vote']

        # Post a message with the team being voted for.
        message = json.dumps({'team': team})
        current_app.extensions['rabbit_queue'].queue_message(message)

        # Rendering the output for index.
        return render_template(
            'index.html',
            last_vote=team,
            teams_competing=TEAMS_COMPETING,
            team_votes_total=vote_total,
        )

    else:
        return render_template('index.html',
            teams_competing=TEAMS_COMPETING,
            team_votes_total=vote_total)


def create_teams():
    """
    Helper method to create teams.
    """
    for x in range(1, 4):
        TEAMS_COMPETING.append('{}'.format(x))


def run_app(app):
    init_app(app)
    app_start.send(app)

    try:
        logging.warning('starting web service')
        ws = gevent.wsgi.WSGIServer(('0.0.0.0', int(5000)), app)
        ws.serve_forever()

    finally:
        logging.info('change this later')

def main():
    app.debug = True
    create_teams()
    run_app(app)
