FROM python:3.6-slim

COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app/

EXPOSE 80

ENTRYPOINT [ "bash","./entrypoint.sh" ]
