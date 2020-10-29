FROM python:3.8

# needed for opencv
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app
CMD uwsgi --spooler artspooler --master --die-on-term --processes 2 --http :80 --module main:app
STOPSIGNAL SIGTERM
