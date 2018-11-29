FROM golang
WORKDIR /tmp/
RUN apt-get update && \
    apt-get install -y libxrender1 && \
    wget --no-check-certificate https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb && \
    dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb; \
    apt -f install -y || exit 0
# RUN apt-get update && apt-get install -y wkhtmltopdf
COPY statement_generator /go/src/statement_generator/
WORKDIR /go/src/statement_generator/
RUN go get ./...
RUN go build main.go
CMD ./main
