FROM node:18.16.0

# 作業ディレクトリを作成
WORKDIR /workspace

# プロジェクトファイルをコピー
COPY . .

# パッケージをインストール
RUN npm install

# Hardhatノードを起動
CMD ["npx", "hardhat", "node"]
