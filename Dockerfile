FROM python:3.7

WORKDIR /app/

RUN apt-get update -y && \
    apt-get install -y gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install dependencies first to keep it cached on file changes
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN ./manage.py collectstatic --no-input
RUN ./manage.py compilemessages
