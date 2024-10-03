FROM node:18.16.0

LABEL maintainer="minabe minabe@student.42tokyo.jp"

# ソースコードをコピー
COPY ./eth /workspace/eth

WORKDIR /workspace/eth

# パッケージをインストール
RUN npm ci

CMD ["/bin/bash", "-c", "npx hardhat compile && npx hardhat node"]
