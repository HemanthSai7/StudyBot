FROM python:3.10.9

COPY ./StudybotAPI .

WORKDIR /

RUN mkdir /.cache

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]