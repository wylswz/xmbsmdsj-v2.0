FROM ubuntu:18.04
# Making working Directory as AlGoLib_bootcamp
WORKDIR /patent

RUN apt update
RUN apt install -y python3-pip 

ADD ./requirements.txt /patent/requirements.txt
RUN pip3 install -r requirements.txt
RUN apt install -y nginx
# Make port 80 available to the world outside this container

