FROM python:3.10-slim

WORKDIR /ads_online


COPY poetry.lock .
COPY pyproject.toml .
RUN pip install --no-cache-dir --no-warn-script-location -U pip &&\
    pip install --no-cache-dir --no-warn-script-location poetry &&\
    poetry config virtualenvs.create false &&\
    poetry install


COPY skymarket/manage.py .
COPY skymarket/ads ads
COPY skymarket/django_media django_media
COPY skymarket/django_static django_static
COPY skymarket/redoc redoc
COPY skymarket/skymarket skymarket
COPY skymarket/fixtures fixtures
COPY skymarket/users users
COPY entrypoint.sh entrypoint.sh


ENTRYPOINT ["bash"git "entrypoint.sh"]