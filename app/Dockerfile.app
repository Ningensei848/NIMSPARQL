FROM node:14.4.0-buster-slim
WORKDIR /App


# パッケージをコピー(このファイルだけ別にして先にインストールしたほうが良い)
COPY ./sparql/package*.json ./
# npm モジュールをインストール
# 必要なツールをインストール
# RUN apt-get -y update && apt-get -y upgrade && apt-get -y install curl
# RUN curl --compressed -o- -L https://yarnpkg.com/install.sh | bash && . ~/.bashrc && yarn install --quiet

RUN npm install -g npm && npm install --quiet

# yarn install --quiet

# instead of clone from remote repository
COPY ./sparql/ App/

