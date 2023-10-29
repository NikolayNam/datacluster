FROM python:3.12.0-bullseye

RUN apt-get install
RUN apt-get update && apt-get install -y \
  bzr \
  cvs \
  git \
  python3-dev \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /api

ENV PYTHONPATH=/api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Сделайте entrypoint.sh исполняемым
RUN chmod +x entrypoint.sh

# Используйте entrypoint.sh вместо прямого запуска приложения
ENTRYPOINT ["./entrypoint.sh"]
