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
RUN cabal update \
  && cabal install cabal-install \
  && mv /root/.cabal/bin/cabal /usr/local/bin/cabal

# Get sources
ARG pandoc_commit=rc/2.8.1
RUN git clone --branch=$pandoc_commit --depth=1 --quiet \
        https://github.com/jgm/pandoc /usr/src/pandoc
RUN git clone --quiet \
        https://github.com/lierdakil/pandoc-crossref.git /usr/src/pandoc-crossref

# Install Haskell dependencies
WORKDIR /usr/src/pandoc
RUN cabal --version \
  && ghc --version \
  && cabal new-update \
  && cabal new-clean \
  && cabal new-configure \
           --flag embed_data_files \
           --flag bibutils \
           --constraint 'hslua +system-lua +pkg-config' \
           --enable-tests \
           . pandoc-citeproc \
  && cabal new-build . pandoc-citeproc
WORKDIR /usr/src/pandoc-crossref
RUN cabal new-configure  \
           --flag embed_data_files \
           --flag bibutils \
           --constraint 'hslua +system-lua +pkg-config' \
           . exe:pandoc-crossref \
  && cabal new-build . exe:pandoc-crossref

# Install Tectonic

RUN apk --no-cache -U add git g++ libressl-dev libssl1.1 libcrypto1.1 fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev

RUN apk --no-cache -U add cargo outils-md5

RUN cargo install --git https://github.com/tectonic-typesetting/tectonic.git tectonic


RUN cp /usr/src/pandoc*/dist-newstyle/build/*/*/pandoc*/x/pandoc*/build/pandoc*/pandoc /usr/bin
RUN cp /usr/src/pandoc*/dist-newstyle/build/*/*/pandoc-citeproc*/build/pandoc-citeproc/pandoc-citeproc /usr/bin
RUN cp /usr/src/pandoc*/dist-newstyle/build/*/*/pandoc*/x/pandoc*/build/pandoc*/pandoc-crossref /usr/bin


FROM alpine AS alpine-pandoc

COPY --from=pandoc-builder /usr/bin/pandoc* /usr/bin/
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
RUN ln -s /root/.cache/Tectonic /data/.cache

WORKDIR /data
ENTRYPOINT ["pancake"]
