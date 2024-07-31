FROM node:18.16.0

# 作業ディレクトリを作成
WORKDIR /workspace

# パッケージリストをコピーしてインストール
COPY package*.json ./
RUN npm install && npm install @nomicfoundation/hardhat-toolbox

# プロジェクトファイルをコピー
COPY . .

# Hardhatノードを起動
CMD ["npx", "hardhat", "node"]
