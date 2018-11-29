FROM golang
RUN go get google.golang.org/grpc && \
    go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway && \
    go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger && \
    go get -u github.com/golang/protobuf/protoc-gen-go && \
    go get github.com/favadi/protoc-go-inject-tag
RUN apt-get update && apt-get install unzip
RUN PROTOC_ZIP=protoc-3.3.0-linux-x86_64.zip && \
    curl -OL https://github.com/google/protobuf/releases/download/v3.3.0/$PROTOC_ZIP && \
    unzip -o $PROTOC_ZIP -d /usr/local && \
    rm -f $PROTOC_ZIP
COPY auth /go/src/Web/auth/
WORKDIR /go/src/Web/auth
RUN protoc -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis -I bio_service/ bio_service/bio.proto --go_out=plugins=grpc:bio_service && \
    protoc -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis -I bio_service/ bio_service/bio.proto --grpc-gateway_out=logtostderr=true:rest_gateway && \
    protoc-go-inject-tag -XXX_skip=sql -input=./bio_service/bio.pb.go
RUN cp bio_service/bio.pb.go rest_gateway/bio.pb.go
RUN go get ./...
RUN go build gateway_server/gateway.go && go build server.go
CMD ./server