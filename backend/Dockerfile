FROM python:3.14.0-alpine
LABEL authors="error"

WORKDIR /backend

# моё дополнение / Артём
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    postgresql-libs

COPY requirements.txt .
RUN pip install -r requirements.txt

#Ещё одно моё дополнение / Артём
RUN apk del gcc musl-dev postgresql-dev

COPY ./source .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
