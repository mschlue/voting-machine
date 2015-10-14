voting_wars
===========

Voting wars, a project to teach dockerizing distributed microservices. 


### Configuration
The configuration of the application is handled through environment variables
using sane default values to enable local development.

* RABBITMQ_HOST - [default: localhost] The host address of rabbitmq.
* RABBITMQ_PORT - [default: 5672] The port number rabbitmq is hosted on.
* RABBITMQ_USERNAME - [default: guest] The username for rabbitmq login.
* RABBITMQ_PASSWORD - [defautl: guest] The password associated with the given username.
* RABBITMQ_EXCHANGE - [default: votes] The rabbitmq exchange to send queued messages to.     
* REDIS_HOST - [default: localhost] Hostname of the redis server.
* REDIS_PORT - [default: 6379] The port number redis is hosted on.
* REDIS_DB - [default: 0] Which database to use inside redis.