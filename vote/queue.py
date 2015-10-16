from kombu import Connection, Producer
import os
import gevent.queue
import logging

class Queue(object):
    """
    Manage connections to rabbitmq.
    """

    def __init__(self):
        self.rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)
        self.rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.rabbitmq_exchange = os.getenv('RABBITMQ_EXCHANGE', 'votes')

        self.queue = gevent.queue.Queue()
        self.create_connection()


    def start(self):
        """
        Start the queue service running.
        """
        greenlets = []
        try:
            logging.debug("starting publish greenlet")
            greenlets.append(gevent.spawn(self.publish_loop))
        except:
            logging.exception("unexpected greenlet exit")
            gevent.killall(greenlets)
            raise

    def create_connection(self):
        """
        Create a connection the the broker.
        """
        self.connection = Connection('amqp://{}:{}@{}:{}//'.format(
            self.rabbitmq_username, self.rabbitmq_password,
            self.rabbitmq_host, self.rabbitmq_port
        ))

        self.producer = Producer(self.connection)

    def queue_message(self, message):
        """
        Add a message to the gevent queue to get published.
        """
        logging.info('Adding message to GEVENT queue to be published.')
        self.queue.put(message)

    def publish_message(self, message):
        """
        Publish a single message to rabbitmq.
        """
        logging.debug("throwing message on the queue.")
        publish = self.connection.ensure(self.producer,
                                         self.producer.publish,
                                         max_retries=3)
        publish(message, routing_key='votes')

    def publish_loop(self):
        """
        Listen to the Gevent queue and publish messages.
        """
        logging.warning('starting queue, waiting for events.')
        for message in self.queue:
            logging.warning("calling publish_message")
            self.publish_message(message)
