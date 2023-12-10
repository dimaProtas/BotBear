FROM python:3.10

WORKDIR .

RUN pip install --upgrade pip

COPY ./ ./

RUN pip install -r requirements.txt
RUN pip install gunicorn