FROM python:3.10.12-alpine3.18  AS build

WORKDIR /app

COPY reqs.txt ./reqs.txt

RUN pip install --no-cache-dir -r reqs.txt

FROM gcr.io/distroless/python3 AS prod

COPY --from=build /venv /venv

COPY . /app

WORKDIR /app

ENTRYPOINT ["main.py"]