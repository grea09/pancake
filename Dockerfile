FROM alpine:latest
RUN apk --no-cache --update add python3 py3-pip inotify-tools librsvg wget bash
RUN ln -s `which python3` /usr/bin/python
RUN ln -s `which pip3` /usr/bin/pip

RUN apk --no-cache --update add git g++ openssl-dev fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev
#RUN apk --no-cache --update add fontconfig harfbuzz harfbuzz-icu icu freetype graphite2 libpng zlib

RUN apk --no-cache --update --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community add cargo ghc cabal outils-md5

RUN cargo install tectonic
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rm -R /root/.cargo/registry

RUN cabal update
RUN cabal install pandoc pandoc-citeproc pandoc-crossref
RUN rm -R /root/.cabal/packages
ENV PATH="/root/.cabal/bin:${PATH}"

COPY .fonts /root/.fonts
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
RUN ln -s /root/.cabal/bin/pandoc-citeproc /root/.pancake/filters/pandoc-citeproc
RUN ln -s /root/.cabal/bin/pandoc-crossref /root/.pancake/filters/pandoc-crossref
RUN ln -s /root/.cache/Tectonic /data

RUN pip install pandocfilters

#RUN mkdir /tmp/pancake
#RUN echo -e "# Initialization\n\nInit latex $\mathbb{Math}$ !" > /tmp/pancake/init.md
#RUN pancake -1 /tmp/pancake/init.md
#RUN rm -R /tmp/pancake

WORKDIR /doc
ENTRYPOINT ["pancake"]
