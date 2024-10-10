FROM python:3.9-slim

WORKDIR /app

COPY fibo.py .

RUN pip install flask requests

CMD ["python", "fibo.py"]