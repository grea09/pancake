FROM alpine

#COPY --from=pandoc/crossref /usr/local/bin/pandoc* /usr/local/bin/
#COPY --from=pandoc/crossref /usr/lib/* /usr/lib/
COPY --from=pandoc/core:2.9.2.1 /usr/bin/pandoc* /usr/local/bin/
COPY --from=pandoc/core:2.9.2.1 /usr/lib/* /usr/lib/
COPY --from=grea09/tectonic /root/.cargo/bin/tectonic /usr/local/bin/
COPY --from=grea09/tectonic /usr/lib/* /usr/lib/

RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache -U add python3 python3-dev py3-pip
RUN ln -s `which python3` /usr/bin/python
#RUN ln -s `which pip3` /usr/bin/pip
RUN pip install -U panflute pip

RUN apk --no-cache -U add lua5.3 lua5.3-lpeg gmp libffi
RUN apk --no-cache -U add libstdc++ libressl3.1-libssl harfbuzz harfbuzz-icu icu fontconfig libpng zlib librsvg
RUN apk --no-cache -U add inotify-tools wget bash git

COPY .fonts /root/.fonts
RUN echo -e "<fontconfig>\n\t<dir>/data/fonts</dir>\n\t<dir>~/.fonts</dir>\n</fontconfig>" >  /etc/fonts/local.conf
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
ENV PYTHONPATH="/root/.pancake/lib:${PYTHONPATH}"
RUN mkdir /data
RUN ln -s /data/.cache /root/.cache/Tectonic

WORKDIR /data
ENTRYPOINT ["pancake"]
