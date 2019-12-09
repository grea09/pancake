FROM alpine AS pandoc-builder

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
ARG pandoc_commit=master
RUN git clone --depth=1 --quiet \
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
RUN cabal new-configure . exe:pandoc-crossref \
  && cabal new-build . exe:pandoc-crossref

# Install Tectonic
RUN echo -e "http://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache -U add git g++ libressl-dev fontconfig-dev harfbuzz-dev icu-dev graphite2-dev libpng-dev zlib-dev

RUN apk --no-cache -U add cargo outils-md5

RUN cargo install --git https://github.com/tectonic-typesetting/tectonic.git tectonic
RUN cp /root/.cargo/bin/tectonic /usr/bin/


FROM pandoc-builder AS pandoc-binaries
RUN find dist-newstyle \
         -name 'pandoc*' -type f -perm +400 \
         -exec cp '{}' /usr/bin/ ';' \
  && strip /usr/bin/pandoc /usr/bin/pandoc-citeproc /usr/bin/pandoc-crossref

FROM alpine AS alpine-pandoc

COPY --from=pandoc-binaries /usr/bin/pandoc* /usr/bin/
COPY --from=pandoc-binaries /usr/bin/tectonic /usr/bin/

RUN apk -U upgrade -a
RUN apk --no-cache update

RUN apk --no-cache -U add python3 python3-dev py3-pip inotify-tools librsvg wget bash
RUN ln -s `which python3` /usr/bin/python
RUN ln -s `which pip3` /usr/bin/pip
RUN pip install -U pandocfilters pip

COPY .fonts /root/.fonts
RUN echo -e "<fontconfig>\n\t<dir>/data/fonts</dir>\n\t<dir>~/.fonts</dir>\n</fontconfig>" >  /etc/fonts/local.conf
COPY .pancake /root/.pancake
RUN chmod +x /root/.pancake/bin -R
ENV PATH="/root/.pancake/bin:${PATH}"
ENV PYTHONPATH="/root/.pancake/lib:${PYTHONPATH}"
RUN ln -s /root/.cache/Tectonic /data/.cache

WORKDIR /data
ENTRYPOINT ["pancake"]
