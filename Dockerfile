FROM python:2
WORKDIR /app

COPY req.txt ./
RUN pip install --no-cache-dir -r req.txt
COPY . .
CMD [ "python", "./kf_consumer.py" ]