FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="Uday Kumar <uday.kumar@bridgeconn.com>"

COPY ./app /app/app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app/app

CMD ["./entrypoint.sh"]