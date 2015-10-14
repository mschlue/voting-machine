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
        logging.debug('initializing redis instance')
        self.REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
        self.REDIS_PORT = os.getenv('REDIS_PORT',  6379)
        self.REDIS_DB = os.getenv('REDIS_DB', 0)

    def start(self):
        """
        Start a redis handler.
        """
        self.create_session()

    def create_session(self):
        """
        Create a session to the Redis server

        :return: A valid Redis session.
        """
        self.redis_session = redis.StrictRedis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB
        )
        logging.debug('Created redis session.')

    def set_key(self, redis_session, key, value):
        """
        Set a key in the redis datastore.
        """
        self.redis_session.set(key, value)

    def get_key(self, key):
        """
        Retrieve a specific key from redis.
        """
        return self.redis_session.get(key)

    def increment_vote(self, team_number):
        """
        Increment the vote count for a specific team.
        """
        logging.debug('')
        self.redis_session.incr(team_number)


