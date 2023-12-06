FROM python:3.10.9

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

COPY --chown=user ./StudybotAPI .

WORKDIR $HOME/

RUN mkdir $HOME/.cache

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]