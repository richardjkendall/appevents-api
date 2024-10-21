FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "-w", "4", "app:app"]