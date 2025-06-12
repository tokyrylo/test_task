1. `mv .env.example .env`

2. `docker-compose build --no-cache`

3. `docker-compose up`

4. `alembic upgrade head`

5. `docker-compose exec app python seed.py`


all tables in src/database.py