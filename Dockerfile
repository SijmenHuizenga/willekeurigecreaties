FROM tiangolo/uwsgi-nginx-flask:python3.8

# needed for opencv
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app



