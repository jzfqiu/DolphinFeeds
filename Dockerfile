FROM python:3.10.4-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src .
CMD [ "python3","-u", "server.py"]