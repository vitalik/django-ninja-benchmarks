FROM python:3.8.2

ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=on

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY common_django_settings.py /common_django_settings.py
COPY app_drf /app_drf
COPY app_flask_marshmallow /app_flask_marshmallow
COPY app_ninja /app_ninja
COPY network_service.py /network_service.py
