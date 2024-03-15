FROM python:3.9

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/. .
COPY app/. .

# Create an empty data.csv file
RUN touch data.csv

CMD [ "python", "./src/server.py" ]
