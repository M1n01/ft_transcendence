FROM node:18.16.0

# ソースコードをコピー
COPY ./eth /workspace/eth
WORKDIR /workspace/eth

# package.jsonとpackage-lock.jsonをコピー
COPY eth/package*.json ./
RUN npm ci

CMD ["/bin/bash", "-c", "npx hardhat compile && npx hardhat node"]
