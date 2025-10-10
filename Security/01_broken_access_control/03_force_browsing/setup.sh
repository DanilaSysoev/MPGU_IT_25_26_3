#!/usr/bin/sh

cd $1

echo "Cleaning..."
rm -vrf $2/migrations
rm -vf db.sqlite3
rm -vrf data
echo "OK"

echo "Running makemigrations..."
python manage.py makemigrations $2
echo "OK"

echo "Running migrate..."
python manage.py migrate
echo "OK"

echo "Running seed_demo..."
python manage.py seed_demo
echo "OK"

echo "Running tests..."
pytest
echo "OK"
