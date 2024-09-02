FROM node:18.16.0

# 作業ディレクトリを作成
WORKDIR /workspace

# package.jsonとpackage-lock.jsonを先にコピー
COPY ./eth/package*.json ./

# 依存関係をインストール
RUN npm install

# プロジェクトディレクトリをコピー
COPY ./eth/ .
COPY ./docker/eth/entrypoint.sh /usr/local/bin/eth-entrypoint.sh

RUN chmod +x /usr/local/bin/eth-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/eth-entrypoint.sh"]
