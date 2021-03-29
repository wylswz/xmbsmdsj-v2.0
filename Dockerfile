FROM python:3

WORKDIR /patent

ADD . /patent
RUN pip3 install -r requirements.txt --proxy http:10.114.114.1:1091
EXPOSE 80
EXPOSE 443
# Make port 80 available to the world outside this container
RUN python manage.py collectstatic --no-input

ENTRYPOINT [ "uwsgi", "-i", "/patent/config/uwsgi.ini" ]