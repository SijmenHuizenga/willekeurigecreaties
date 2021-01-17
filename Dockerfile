FROM python:3.8

# needed for opencv
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app
RUN mkdir artspooler

# ensure stdout is flushed immediately
ENV PYTHONUNBUFFERED=1

CMD python main.py
STOPSIGNAL SIGTERM
