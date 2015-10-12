import logging
import redis
import os


class RedisHandler():
    """
    Class for handling redis interactions
    """

    def __init__(self):
        """
        Configures the connection to the redis server
        using environment, with localhost defaults.
        """
        print "did initialize"
        self.REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
        self.REDIS_PORT = os.getenv('REDIS_PORT',  6379)
        self.REDIS_DB = os.getenv('REDIS_DB', 0)

    def create_session(self):
        """
        Create a session to the Redis server

        :return: A valid Redis session.
        """
        redis_session = redis.StrictRedis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB
        )
        logging.info('Created redis session.')
        return redis_session

    def set_key(self, redis_session, key, value):
        """
        Set a key in the redis datastore.
        """
        redis_session.set(key, value)

    def increment_vote(self, redis_session, team_number):
        """
        Increment the vote count for a specific team.
        """
        redis_session.incr(team_number)


