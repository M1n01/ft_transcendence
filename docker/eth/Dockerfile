FROM node:18.16.0

LABEL maintainer="minabe minabe@student.42tokyo.jp"

# ソースコードをコピー
COPY ./eth /workspace/eth
WORKDIR /workspace/eth

# package.jsonとpackage-lock.jsonをコピー
COPY eth/package*.json ./
RUN npm ci && \
	npm install --save-dev hardhat

CMD ["/bin/bash", "-c", "npx hardhat compile && npx hardhat node"]
