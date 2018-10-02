FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    xinetd \
    ejabberd \
    libgloox15 \
    libflite1 \
    libpng16-16 \
    libqrencode3 \
    libzbar0 \
    libmagick++-6.q16-7

COPY service.conf /service.conf
COPY vchat /vchat
COPY vbot /vbot
RUN chmod 755 /vchat /vbot && touch /flag && chmod 644 /flag && echo -n "gift" | shasum -a 512 | cut -c 1-48  > /flag

EXPOSE 2555
ENV VCHAT_SERVER ooo.vchat
ENV VCHAT_MESSAGE hello
CMD ["xinetd", "-dontfork", "-f", "/service.conf"]
