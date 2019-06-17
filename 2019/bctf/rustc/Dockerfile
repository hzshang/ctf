from rust:1.34.2

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd build-essential ssh
RUN apt-get install python3

RUN rustup default nightly

RUN groupadd ruscas && \
    useradd -g ruscas ruscas -m

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY . /app
COPY ./flag /flag

WORKDIR /app

CMD exec /bin/bash -c "/etc/init.d/xinetd start; trap : TERM INT; sleep infinity & wait"

EXPOSE 50806
