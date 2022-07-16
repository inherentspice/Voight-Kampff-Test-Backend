FROM python:3.8.12-buster

WORKDIR /VoightKampffTestBackend

COPY checkpoint/run2  /VoightKampffTestBackend/checkpoint/run1
COPY requirements.txt /VoightKampffTestBackend//requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY api  /VoightKampffTestBackend/api
COPY VoightKampffTestBackend/response_generator.py  /VoightKampffTestBackend/VoightKampffTestBackend/response_generator.py

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT

COPY wagon-bootcamp-354400-769b4ba3f103.json /credential.json
