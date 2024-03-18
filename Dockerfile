FROM python:3.11.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./config/requirements.txt /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/apps/api/

# COPY ./scripts/entrypoint.sh /entrypoint.sh

# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]


# https://chat.openai.com/share/3dfedd88-3d94-4fb9-a4d4-eb6e24e2baa5