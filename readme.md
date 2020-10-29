# Willekeurigecreaties
translated: Random Creations

![header.png](header.png)

A web-page that shows recycled #art 

## Run it locally

1. Create yourself a folder `app/media` and `app/art`.
2. Put a lot of images in `media` and give the program read access.
3. Give the program write access to output.
4. Install python requirements: `pip install requirements.txt`
5. To run it, go itno `app` and `uwsgi --spooler artspooler --master --processes 2 --http :9090 --module main:app`
6. Visit `localhost:9090` to view it!

## Deploy it in production

1. Build it: `docker build -t willekeurigecreaties .`
2. Run it: `docker run --rm --name willekeurigecreaties -v $(pwd)/media:/app/media -v $(pwd)/art:/app/art -p 80:80 willekeurigecreaties`