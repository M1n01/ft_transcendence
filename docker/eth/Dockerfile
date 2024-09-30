FROM node:18.16.0

# ソースコードをコピー
COPY ./eth /workspace/eth
WORKDIR /workspace/eth

# package.jsonとpackage-lock.jsonをコピー
COPY eth/package*.json ./
RUN npm ci

RUN npm install --save-dev hardhat

CMD ["/bin/bash", "-c", "npx hardhat compile && npx hardhat node"]
