FROM alpine:latest
RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk --no-cache --update add python3 python3-dev py3-pip inotify-tools librsvg wget bash
RUN ln -s `which python3` /usr/bin/python
RUN ln -s `which pip3` /usr/bin/pip

RUN apk --no-cache --update add git g++ openssl-dev fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev
#RUN apk --no-cache --update add fontconfig harfbuzz harfbuzz-icu icu freetype graphite2 libpng zlib

RUN apk --no-cache --update add cargo ghc cabal outils-md5

RUN cargo install tectonic
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rm -R /root/.cargo/registry

RUN cabal update
RUN cabal install Cabal
RUN cabal new-install pandoc pandoc-crossref pandoc-citeproc
RUN rm -R /root/.cabal/packages
ENV PATH="/root/.cabal/bin:${PATH}"

RUN pip install -U pandocfilters ruamel.yaml pip

RUN echo -e "<fontconfig>\n\t<dir>/doc/fonts</dir>\n\t<dir>~/.fonts</dir>\n</fontconfig>" >  /etc/fonts/local.conf
COPY .fonts /root/.fonts
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
RUN ln -s /root/.cabal/bin/pandoc-citeproc /root/.pancake/filters/3.pandoc-citeproc
RUN ln -s /root/.cabal/bin/pandoc-crossref /root/.pancake/filters/2_pandoc-crossref
RUN ln -s /root/.cache/Tectonic /data

WORKDIR /doc
CMD pancake
