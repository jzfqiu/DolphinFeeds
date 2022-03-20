FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir src
COPY ./src ./src
CMD [ "python3", "server.py"]