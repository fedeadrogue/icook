FROM python:3.8.12-slim
COPY icook /icook
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
COPY setup.py setup.py
RUN pip install .
CMD uvicorn icook.api.fast:app --host 0.0.0.0 --port $PORT
