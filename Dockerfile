FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip 

RUN pip install pip==7.1.2

RUN mkdir /voting_wars
ADD . /voting_wars/

WORKDIR /voting_wars/

RUN pip install dist/voting_wars-*

CMD voting-web
