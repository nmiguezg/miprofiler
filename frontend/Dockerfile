FROM node:alpine

WORKDIR /usr/app

COPY ./package*.json ./

RUN pwd

RUN npm install

COPY ./ ./

RUN npm run build

EXPOSE 3000

ENV DOCKERIZE_VERSION v0.7.0

RUN apk update --no-cache \
    && apk add --no-cache wget openssl \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apk del wget

# CMD ["dockerize", "-wait", "tcp://profilers:5000", "npm", "run", "dev"]