FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
  netcat-openbsd chromium chromium-driver \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

ENV SCRIPTLATTES_CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    SCRIPTLATTES_CHROME_BINARY=/usr/bin/chromium

COPY . .

# Ensure entrypoint is executable inside the image
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
