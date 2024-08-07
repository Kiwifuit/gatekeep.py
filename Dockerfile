FROM python:3.12.4-alpine

WORKDIR /srv

COPY . .

RUN pip install -r requirements.txt
ENTRYPOINT [ "/usr/local/bin/python", "src/main.py" ]
