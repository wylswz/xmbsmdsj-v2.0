# Simple Apache2 Django Backend

This project is my personal website written in Python (Django + Restframework). Both back-end and front-end are integrated inside.

## Start a Django server

To start the backend, makesure you have properly installed Python3 and pip properly.

```bash
# proj_dir: where the manage.py is located

$ sudo apt update
$ sudo apt install python3-pip python3-venv
```

Start a virtual env and install the dependancies:

```
$ cd proj_dir
$ python3 -m venv ./venv
$ pip3 install -r requirements.txt
```

Migrate the database (init superuser if implemented)
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py initsuperuser # not necessarily available
```

Start the project on localhost:8000 using Django server

```
$ python3 manage.py runserver
```

## Use Docker with Apache2 to deploy https server
This part is not applicable for everyone cuz I'm using my own docker container. So it only works for my domain name. But if you only wanna deploy deploy http service, that would be fine.

The following paragraphs will explain how to write apache configuration files.

First step is to install apache2 on your machine
```
$ sudo apt install apache2 apache2-dev
```

Now the apache2 server is installed on your machine. You can start it using
```
$ sudo service apache2 start
```
The default files served by apache2 is placed at ```/var/www/``` on your machine. But what we want is to serve Django project using apache. Here we need a module to connect apache2 with wsgi interface provided by Django, which is called **mod_wsgi**

In your virtual env, install that module by
```
$ pip3 install mod_wsgi
```
Of course you install it out side the venv, as long as in the place you can easily find, that would be perfectly fine.

Next, generate the apache2 config string by
```
$ mod_wsgi-express module-config
```
and add the output lines to /etc/apache2/apache2.conf, it would be like this:

```apacheconf
WSGIPythonHome "some_path"
# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
LoadModule wsgi_module "some_prefix/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
```

Now that the mod_wsgi is configured successfully, next specify some details of your django project

```apacheconf
<VirtualHost *:80>
# Http config
WSGIDaemonProcess proj-name python-path=/proj-home
WSGIProcessGroup proj-name
WSGIScriptAlias / /proj/mainapp/wsgi.py
Alias /media/ /proj/media/
Alias /static/ /proj/staticfiles/
    <Directory /proj/staticfiles>
        Require all granted
    </Directory>
    <Directory /proj/media>
        Require all granted
    </Directory>
<Directory /proj/app>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
</VirtualHost>

```

Put this block in ```/etc/apache2/apache2.conf``` or ```/etc/apache2/sites-available/000-default.conf```
 and restart the apache2 server, your django app should be served properly.

 The following content is for https deployment.

There are 3 main differences between http and https deployment

- Different port: HTTPS uses 443
- Certification: HTTPS needs certificate to work. It can be self signed, or signed by third-party. Usually need to pay a small amount of money.
- Extra configurations

First, get your own certificate. Just generate csr and key, then go get a cert. Please keep the .key file, .crt and .pem files well, try not to lose them, or your website won't be working.

Put the cert and key files somewhere you can find, you will need to specify the path in apache2 configuration file.

```apacheconf
<VirtualHost *:443>
LoadModule wsgi_module "/patent/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
WSGIDaemonProcess patent python-path=/patent
WSGIProcessGroup patent
WSGIScriptAlias / /proj/app/wsgi.py
Alias /media/ /proj/media/
# Serve media files here
Alias /static/ /proj/staticfiles/
# Serve static files here
    <Directory /proj/staticfiles>
        Require all granted
    </Directory>
    <Directory /proj/media>
        Require all granted
    </Directory>
<Directory /proj/patent>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
RequestReadTimeout header=1000 body=3000
LimitRequestFieldSize 65536000
# Limits the size of the HTTP request header allowed from the client
LimitRequestLine 65536000
# Limit the size of the HTTP request line that will be accepted from the client
LimitRequestBody 83886080
# Restricts the total size of the HTTP request body sent from the client
SSLCertificateFile /your.crt
SSLCertificateKeyFile /your.key
<Location />

SSLRenegBufferSize 65536000
# SSL buffer size
SSLRequireSSL On
SSLVerifyClient optional
SSLVerifyDepth 1
SSLOptions +StdEnvVars +StrictRequire
</Location>
</VirtualHost>

```

Restart your server and have fun

## Docker deployment

There are basically 2 ways of deploying this project using docker.

- Use docker-compose build to get everything configured
- Use pre-configured docker images

I would definitely prefer second one, because installing libraries, changing configures in Dockerfile is quite conplex, and building the image everytime can be quite time consuming.

What I did is doing all the configurations above and encapsulate the changes to docker image. 

Therefore the Dockerfile is quite simple:
```dockerfile
FROM wylswz/mysite:https
# Making working Directory as AlGoLib_bootcamp
WORKDIR /patent

# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 443
```

and the docker-compose file
```yaml
version: '2'

services:
  
    

  web:
    build: .

    volumes:
      - /var/log/apache2d/:/var/log/apache2/
      - .:/proj
      - /data/media:/proj/media
      - /data/db/db.sqlite3:/proj/db.sqlite3
    
    command: bash -c "chown -R www-data . && pip3 install -r requirements.txt && python3 manage.py collectstatic --noinput  && yes | python3 manage.py migrate  && service apache2 start && sleep infinity"
    ports:
      - "80:80"
      - "443:443"
    tty: true
    stdin_open: true 

```

If you want to execute some additional operations like create the superuser for your server, just attach into the container using

```bash
$ docker exec -it your_web_container_id bash
```

