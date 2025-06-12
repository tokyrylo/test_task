mv .env.example .env

docker-compose build --no-cache

docker-compose up

all tables in src/database.py