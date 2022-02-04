FROM python:3.8-slim-buster

RUN apt update && apt install curl -y

WORKDIR /src

COPY requirements.txt requirements.txt

COPY source.txt source.txt

COPY main.py main.py

RUN pip3 install -r requirements.txt

RUN rm -rf /bin

ENTRYPOINT ["python3", "main.py"]

CMD ["source.txt"]

