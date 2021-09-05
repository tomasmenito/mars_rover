FROM python:3.9.6

RUN pip install poetry

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install

ADD . /app/

ENTRYPOINT ["bash"]
