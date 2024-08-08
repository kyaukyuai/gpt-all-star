FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  git \
  libjson-c-dev \
  libwebsockets-dev \
  curl \
  && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/tsl0922/ttyd.git && \
  cd ttyd && mkdir build && cd build && \
  cmake .. && \
  make && make install

ENV NVM_DIR /root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
  && . "$NVM_DIR/nvm.sh" \
  && nvm install node \
  && nvm use node

WORKDIR /usr/src/app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root --no-dev

EXPOSE 7681
CMD ["ttyd", "-W", "bash"]
