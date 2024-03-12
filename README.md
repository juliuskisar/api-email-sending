# FastAPI Dev Challenge

## Virtual Environment Mode

First, create your virtual environment:

```bash
$ python3 -m venv venv

```

Then, activate your virtual environment:

```bash
$ source venv/bin/activate
```

Then, install dependencies:

```bash
$ pip install -r requirements.txt
```

Then, run the application:

```bash
$ uvicorn main:app --reload
```

## Docker Mode

### Install Docker 

Just select your OS and download [here](https://www.docker.com/products/docker-desktop)

### Build and run the container application

> Run this commands os the base path of this project

If you in an UNIX based OS, just type:

```
$ docker build --platform linux/amd64 -t fastapi-dev-challenge-docker .
$ docker run --platform linux/amd64 -d -p 8091:8081 -v $(pwd):/app fastapi-dev-challenge-docker
```

If you in a Windows OS `PowerShell`, then type:

```
$ docker build --platform linux/amd64 -t fastapi-dev-challenge-docker .
$ docker run --platform linux/amd64 -d -p 8091:8081 -v ${PWD}:/app fastapi-dev-challenge-docker
```

Or if you using Windows with `CMD`, type:

```
$ docker build --platform linux/amd64 -t fastapi-dev-challenge-docker .
$ docker run --platform linux/amd64 -d -p 8091:8081  -v %cd%:/app fastapi-dev-challenge-docker
```

If you have list of `environment` variables use:

```
$ docker run --platform linux/amd64 -d -p 8091:8081 -v $(pwd):/app --env-file ./.env fastapi-dev-challenge-docker
```

Now just access [http://localhost:8091](http://localhost:8091)
