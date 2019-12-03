FROM alpine:latest
RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk --no-cache --update add python3 python3-dev py3-pip inotify-tools librsvg wget bash
RUN ln -s `which python3` /usr/bin/python
RUN ln -s `which pip3` /usr/bin/pip

RUN apk --no-cache --update add git g++ openssl-dev fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev

RUN apk --no-cache --update add cargo ghc cabal outils-md5

RUN cargo install --git https://github.com/tectonic-typesetting/tectonic.git tectonic
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rm -R /root/.cargo/registry

RUN cabal new-update
RUN cabal new-install Cabal
RUN cabal new-install pandoc pandoc-citeproc pandoc-crossref
RUN rm -R /root/.cabal/packages
ENV PATH="/root/.cabal/bin:${PATH}"

RUN pip install -U pandocfilters pip

COPY .fonts /root/.fonts
RUN echo -e "<fontconfig>\n\t<dir>/doc/fonts</dir>\n\t<dir>~/.fonts</dir>\n</fontconfig>" >  /etc/fonts/local.conf
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
ENV PYTHONPATH="/root/.pancake/lib:${PYTHONPATH}"
RUN ln -s /root/.cabal/bin/pandoc-crossref /root/.pancake/filters/3_pandoc-crossref
RUN ln -s /root/.cabal/bin/pandoc-citeproc /root/.pancake/filters/5_pandoc-citeproc
RUN ln -s /root/.cache/Tectonic /data

WORKDIR /doc
CMD pancake
