FROM ubuntu:20.04

WORKDIR /patent
RUN apt update
RUN apt install -y python3-pip 

ADD ./requirements.txt /patent/requirements.txt
RUN pip3 install -r requirements.txt
# Make port 80 available to the world outside this container

ENTRYPOINT [ "uwsgi", "-i", "/patent/config/uwsgi.ini" ]