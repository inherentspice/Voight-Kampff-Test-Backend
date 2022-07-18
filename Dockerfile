FROM python:3.8.12-buster
RUN rm ~/.cache/pip -rf
WORKDIR /VoightKampffTestBackend

COPY checkpoint/run2  /VoightKampffTestBackend/checkpoint/run2
COPY requirements.txt /VoightKampffTestBackend/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY api/fast.py /VoightKampffTestBackend/api/fast.py
COPY VoightKampffTestBackend/response_generator.py  /VoightKampffTestBackend/VoightKampffTestBackend/response_generator.py

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT

COPY wagon-bootcamp-354400-769b4ba3f103.json /credential.json
