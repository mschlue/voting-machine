FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip 

RUN pip install pip==7.1.2

RUN mkdir /voting-maching
ADD . /voting-machine/

WORKDIR /voting-machine/

RUN pip install dist/voting-machine-0.1.0.tar.gz

CMD voting-web
