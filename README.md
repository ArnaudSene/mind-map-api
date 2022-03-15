# Mind map API 

This is a light API powered by [FastAPI](https://fastapi.tiangolo.com/) with no persistent data.


First clone the repository, 

then go in mind-map-api/

```
cd mind-map-api/
```

## To run locally on your machine

Install dependencies

```shell
pip install -r requirements.txt
```

Start the apps by running:

```bash
bash run.sh
```

## To run through a container with Docker

> Docker must be installed on your machine!


Build the Docker image named `fastapi_img`

```shell
docker build -t fastapi_img .
```

Run the container named `fastapi_container`

```shell
docker run -d --name fastapi_container -p 80:80 fastapi_img
```

## Navigate to mind map

### Locally on your machine:

Root apps: http://127.0.0.1:8000

API: http://127.0.0.1:8000/docs

### Through your container 

Retrieve the Server's IP address where the container is running

Root apps: http:<your_IP_Address>

API: http:<your_IP_Address>/docs
