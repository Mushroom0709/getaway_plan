#!/bin/sh
set -e

# Wait for MySQL to be ready
echo "Waiting for MySQL..."
python3 -c "
import asyncio
import aiomysql
import os

async def wait():
    while True:
        try:
            conn = await aiomysql.connect(
                host=os.environ.get('DB_HOST', 'db'),
                port=3306,
                user='root',
                password=os.environ.get('MYSQL_ROOT_PASSWORD', 'change_me'),
                db='getaway_plan'
            )
            conn.close()
            print('MySQL is ready!')
            break
        except Exception as e:
            print(f'Waiting for MySQL: {e}')
            await asyncio.sleep(1)

asyncio.run(wait())
"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the API server
echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
