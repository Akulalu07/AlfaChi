FROM python:3.14.0-alpine
LABEL authors="error"

WORKDIR backend

COPY main.py .
COPY requests.txt .


RUN pip install -r requests.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
