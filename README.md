# ft_transcendence

## 目次

- [使用技術について](#使用技術について)
- [環境構築](#環境構築)
- [ディレクトリ構成](#ディレクトリ構成)
- [Gitの運用](#gitの運用)

## 使用技術について
### nodeバージョン
- node 
- npm 

### フロントエンド
- VanillaJS
- Bootstrap

### バックエンド
- Django

### ミドルウェア
- Docker
- Nginx
- PostgreSQL
- Docker-compose

## 環境構築
### Visual Studio Code 拡張機能
- Prettier

## クローン
```
$ git clone https://github.com/M1n01/ft_transcendence.git
```

## ローカル立ち上げまで
```
# 環境変数ファイルの作成
$ cp .env.sample .env

# パッケージのインストール
$ npm install

# ローカル環境の立ち上げ
$ make up
```

下記のローカル環境にアクセスできればOK

http://localhost:3000/

## ディレクトリ構造

## Gitの運用
### ブランチについて
mainとfeatureブランチで運用する。

|ブランチ名|役割|派生元|マージ先|
|:---:|:---:|:---:|:---:|
|main|本番環境|-|-|
|feature/*|機能開発|main|main|

### コミットメッセージの記法
```
fix: バグ修正
feat: 新機能追加
update: 機能更新
change: 仕様変更
perf: パフォーマンス改善
refactor: コードのリファクタリング
docs: ドキュメントのみの変更
style: コードのフォーマットに関する変更
test: テストコードの変更
revert: 変更の取り消し
chore: その他の変更
```
