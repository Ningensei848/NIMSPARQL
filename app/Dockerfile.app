# ------------------------------ Build Stage ----------------------------------
FROM node:14.5.0-alpine as builder
RUN apk update && apk add git python make g++
# RUN git clone https://github.com/Ningensei848/EasySparql.git
WORKDIR EasySparql
RUN yarn install
RUN yarn build

# for local development only ---------------------------
# WORKDIR EasySparql
# COPY ./EasySparql/package.json /EasySparql/package.json
# RUN yarn install
# COPY ./EasySparql/ /EasySparql/
# RUN yarn build

# ------------------------------ Prodction Stage ------------------------------
FROM node:14.5.0-alpine
WORKDIR /App
COPY --from=builder /EasySparql /App
