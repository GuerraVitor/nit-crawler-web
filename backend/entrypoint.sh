#!/bin/bash
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
until nc -z "${DB_HOST}" "${DB_PORT}"; do
	sleep 0.5
done
echo "Database is ready!"

echo "Running makemigrations..."
python manage.py makemigrations

echo "Running migrate..."
python manage.py migrate --noinput

SCRAPY_OUTPUT_PATH=${SCRAPY_OUTPUT_PATH:-/data/scrapy_output}
if [ -d "${SCRAPY_OUTPUT_PATH}" ]; then
	echo "Importing Scrapy output from ${SCRAPY_OUTPUT_PATH}..."
	python manage.py import_scrapy_batch --path "${SCRAPY_OUTPUT_PATH}"
else
	echo "No Scrapy output folder found at ${SCRAPY_OUTPUT_PATH}, skipping import."
fi

echo "Starting Django development server..."
exec "$@"
