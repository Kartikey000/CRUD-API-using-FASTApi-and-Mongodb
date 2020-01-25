FROM python:3.6.9-alpine3.10

RUN mkdir /app

COPY ./requirement.txt ./app/requirement.txt

WORKDIR /app
ENV MONGO_CONNECTION=mongo
RUN apk update && apk upgrade && apk add --no-cache curl bash gcc g++ libc-dev unixodbc-dev make linux-headers git openssh libffi-dev

RUN pip3 install -r requirement.txt

COPY . /app/

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]