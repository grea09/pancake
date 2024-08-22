FROM alpine

COPY --from=pandoc/core:2.19.2.0 /usr/local/bin/pandoc* /usr/local/bin/
COPY --from=pandoc/core:2.19.2.0 /usr/lib/* /usr/lib/

RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache -U add python3 python3-dev py3-pip tectonic
RUN pip install -U panflute --break-system-packages

RUN apk --no-cache -U add lua5.3 lua5.3-lpeg gmp libffi
RUN apk --no-cache -U add libstdc++ libressl3.8-libssl harfbuzz harfbuzz-icu icu fontconfig libpng zlib librsvg
RUN apk --no-cache -U add inotify-tools wget bash git

COPY .fonts /root/.fonts
RUN echo -e "<fontconfig>\n\t<dir>/data/fonts</dir>\n\t<dir>~/.fonts</dir>\n</fontconfig>" >  /etc/fonts/local.conf
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
ENV PYTHONPATH="/root/.pancake/lib"
RUN mkdir /data
RUN ln -s /data/.cache /root/.cache/Tectonic

WORKDIR /data
ENTRYPOINT ["pancake"]
