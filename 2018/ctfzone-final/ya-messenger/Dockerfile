FROM python:3.7-stretch
WORKDIR /app
COPY setup.py .
COPY challenge/__init__.py challenge/__init__.py
COPY challenge/common challenge/common
COPY challenge/grpc challenge/grpc
COPY challenge/node challenge/node
RUN apt-get update && \
    apt-get install -y libgmp3-dev libmpfr-dev libmpc-dev
RUN pip install .
CMD ["node-server"]
