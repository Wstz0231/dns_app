FROM python:3.9-slim

WORKDIR /app

COPY user.py .

RUN pip install flask requests

CMD ["python", "user.py"]