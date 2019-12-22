FROM alpine AS pandoc-builder

RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache add \
         alpine-sdk \
         bash \
         ca-certificates \
         cabal \
         fakeroot \
         ghc \
         git \
         gmp-dev \
         lua5.3-dev \
         pkgconfig \
         zlib-dev

# Install newer cabal-install version
COPY cabal.root.config /root/.cabal/config
RUN cabal new-update \
  && cabal new-install cabal-install \
  && mv /root/.cabal/bin/cabal /usr/local/bin/cabal


# Install Haskell dependencies
RUN cabal --version \
  && ghc --version
RUN cabal new-clean

RUN cabal new-install pandoc pandoc-citeproc \
#      --install-method=copy --installdir=/usr/bin \
      --flag embed_data_files \
      --flag bibutils \
      --constraint 'hslua +system-lua +pkg-config'

RUN cabal new-install pandoc-crossref \
#            --install-method=copy --installdir=/usr/bin \
            --flag embed_data_files

# Install Tectonic

RUN apk --no-cache -U add cargo g++ outils-md5

RUN apk --no-cache -U add git libressl-dev libssl1.1 libcrypto1.1 fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev

# --git https://github.com/tectonic-typesetting/tectonic.git
RUN cargo install tectonic

FROM alpine AS alpine-pandoc

COPY --from=pandoc-builder /root/.cabal/bin/* /usr/bin/
COPY --from=pandoc-builder /root/.cargo/bin/tectonic /usr/bin/

RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache -U add python3 python3-dev py3-pip
RUN ln -s `which python3` /usr/bin/python
RUN ln -s `which pip3` /usr/bin/pip
RUN pip install -U pandocfilters pip

RUN apk --no-cache -U add lua5.3 lua5.3-lpeg gmp
RUN apk --no-cache -U add libstdc++ libressl3.0-libssl harfbuzz harfbuzz-icu icu fontconfig libpng zlib librsvg
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
