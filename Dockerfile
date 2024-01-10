
FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE  5000
ENV FLASK_APP=app.py
CMD ["flask", "run","--port","5000","--host", "0.0.0.0"]
