from flask import Flask, render_template, request, current_app
import argparse
import os
import retrying
import logging
import gevent.wsgi

from vote import queue
from vote.signals import app_start

app = Flask(__name__)

TEAMS_COMPETING = []


def init_app(app):
    """
    Initialize the rabbitmq extension.
    """
    rabbit_queue = queue.Queue()
    app.extensions['rabbit_queue'] = rabbit_queue


# Template for starting multiple extensions.
@app_start.connect
def start_producers(app, **kwargs):
    producers = [
        app.extensions.get('rabbit_queue')  # ,
        # Add redis extension here
    ]

    for producer in producers:
        if producer:
            producer.run_queue()


@app.route('/', methods=['GET', 'POST'])
def place_vote():
    """
    Main page,
    :return: rendering a page with the status message of the vote for POST
    :return: rendering the default voting wars page for GET requests
    """
    if request.method == 'POST':
        team = request.form['vote']

        logging.warning('WTF...')
        # Post a message with the team being voted for.
        current_app.extensions['rabbit_queue'].queue_message(team)

        # Rendering the output for index.
        return render_template(
            'index.html',
            last_vote=team,
            teams_competing=TEAMS_COMPETING
        )

    else:
        return render_template('index.html',
            teams_competing=TEAMS_COMPETING)

@app.route('/votes')
def votes():
    """
    app route to show the results of voting

    :return: rendered template of the voting results
    """
    temp = redis_server.keys(pattern='*')
    for t in temp:
        print "KEY: " + t + " Value: " + str(redis_server.get(t))

    team_keys = redis_server.keys(pattern='*')

    team_votes_total = {}
    for key in team_keys:
        team_votes_total[key] = redis_server.get(key)

    return render_template("results.html",
        team_votes_total = team_votes_total
    )


def create_teams():
    """
    Helper method to create teams.
    """
    for x in range(1, 15):
        TEAMS_COMPETING.append('Team: {}'.format(x))


def run_app(app):
    init_app(app)
    app_start.send(app)

    try:
        logging.warning('starting the web service')
        ws = gevent.wsgi.WSGIServer(('0.0.0.0', int(5000)), app)
        ws.serve_forever()
        logging.warning('that didnt block')

    finally:
        logging.info('change this later')

if __name__ == "__main__":
    app.debug = True
    create_teams()
    run_app(app)
