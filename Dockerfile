FROM python:3.9-slim
ENV BOT_TOKEN="6794114619:AAFGkIg_X29N0ByNLg7Zil24_e9h8pPU4-k"
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /app/post_tmp
CMD ["python", "main.py"]