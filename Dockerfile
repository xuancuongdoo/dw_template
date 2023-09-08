FROM python:3.10-slim-bullseye


RUN aapt-get update && \
  apt-get install -y --no-install-recommends \
  libpq-dev \
  gcc \
  make \
  bbuild-essential \
  default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir  -r requirements.txt /app/requirements.txt
COPY . /app


EXPOSE 5000

CMD ["python3", "server.py"]
