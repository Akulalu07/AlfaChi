FROM python:3.13-slim
LABEL authors="error"

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./source .
CMD ["python", "./main.py"]
