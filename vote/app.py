from flask import Flask, render_template, request, Blueprint, current_app
import argparse
import os
import retrying

from vote import queue

app = Flask(__name__)

TEAMS_COMPETING = []

@app.route('/', methods=['GET', 'POST'])
def place_vote():
    """
    Main page,
    :return: rendering a page with the status message of the vote for POST
    :return: rendering the default voting wars page for GET requests
    """
    if request.method == 'POST':
        team = request.form['vote']

        # post a message with the team being voted for.
        rabbit_queue = queue.Queue()
        rabbit_queue.run()
        rabbit_queue.queue_message(team)

        # Rendering the output for index
        return render_template(
            'index.html',
            last_vote=team,
            teams_competing=TEAMS_COMPETING
        )

    else:
        return render_template('index.html',
            teams_competing=TEAMS_COMPETING)


# from . import redis_handler

# test = redis_handler.RedisHandler()
# print test.REDIS_HOST
# redis_session = test.create_session()

# test.create_teams(redis_session, 10)


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


#@blueprint.route('/vote/<int:team_vote>', methods=['PUT'])
def api_vote(team_vote):
    """
    Api to allow teams to post votes.
    """
    print "WE DID STUFF!!!"
    current_vote_count = redis_server.get(team)
    if current_vote_count is None:
        current_vote_count = int(1)
    else:
        current_vote_count = int(current_vote_count) + 1
        redis_server.set(team, current_vote_count)

def create_teams():
    """
    Helper method to create teams.
    """
    for x in range(1, 10):
        TEAMS_COMPETING.append('Team: {}'.format(x))

def create_queue():
    """
    Helper method to create and instantiate a queue object.
    """
    rabbit_queue = queue.Queue()
    rabbit_queue.run()
    return queue

def init_app(app):
    rabbit_queue = create_queue()
    app.extension['queue'] = rabbit_queue
    return app

if __name__ == "__main__":
    app.debug = True
    # create_teams()
    # app = init_app(app)
    rabbit_queue = queue.Queue()
    rabbit_queue.run()
    rabbit_queue.queue_message('test_message')
    app.run()

