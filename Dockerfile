FROM python:3.11-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src

CMD ["uvicorn", "src.main:src", "--host", "0.0.0.0", "--port", "8000", "--reload"]
