FROM python:3.11


COPY . .

RUN pip install -r requirements.txt
WORKDIR src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]