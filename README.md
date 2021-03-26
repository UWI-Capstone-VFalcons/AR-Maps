# AR-Maps
An augmented reality directional system made specifically for an area

## Dependencies
- Python 3.3 and above
- python3 venv
- Flask 
- Node.js
- Vue 
- Vue-cli

## Getting Started 

### change to the backend directory
```
cd back-ar-maps
```

### Setup environment
```
python -m venv venv
```

**To Activate Virtual environment**
```
source venv/bin/activate (linux)

venv\Scripts\activate (Windows)
```
### install Flask Requirements
```
pip install -r requirements.txt 
```
- If a new python package is added refresh the requirments filr with 
```
pip freeze > requirements.txt
pipenv update
```

### Run services
Run both services in two separate terminals

**Run Flask backend app**
```
python run.py
```

**Run Node frontend app**
```
cd front-ar-maps
npm install
npm run serve
```

## Flask commands

### run migration on databse

This is necessary in order to update the databse whenever a change is made to it

```
./miigrate.sh
```

### run tests

```
pytest -v

or for specific tests

pytest test-folder -v

```
### To add heroku app remote 
```
heroku git:remote -a uwi-ar-maps
```

## Docker Image

### Build image for heroku registry
```
docker build -t registry.heroku.com/uwi-ar-maps/web .
```
### Test Image locally

**Start the docker iamge**
```
docker-compose up

or

docker-compose up -d (in background)
```

**stop the docker image**
```
docker-compose down
```

### deploy image to heroku

```
heroku container:login

docker push registry.heroku.com/uwi-ar-maps/web

heroku container:release --app uwi-ar-maps web
```

