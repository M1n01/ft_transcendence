# ft_transcendence

## 目次

- [ft\_transcendence](#ft_transcendence)
  - [目次](#目次)
  - [使用技術について](#使用技術について)
    - [nodeバージョン](#nodeバージョン)
    - [フロントエンド](#フロントエンド)
    - [バックエンド](#バックエンド)
    - [ミドルウェア](#ミドルウェア)
  - [環境構築](#環境構築)
    - [Visual Studio Code 拡張機能](#visual-studio-code-拡張機能)
    - [クローン](#クローン)
    - [各環境の立ち上げ](#各環境の立ち上げ)
    - [アクセス方法](#アクセス方法)
  - [ディレクトリ構造](#ディレクトリ構造)
  - [Gitの運用](#gitの運用)
    - [ブランチについて](#ブランチについて)
    - [コミットメッセージの記法](#コミットメッセージの記法)

## 使用技術について

### nodeバージョン

- node v22.3.0
- npm v10.8.1

### フロントエンド

- VanillaJS
- Bootstrap

### バックエンド

- Django
- Solidity

### ミドルウェア

- Docker
- Nginx
- PostgreSQL
- Docker-compose

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境構築

### Visual Studio Code 拡張機能

- Prettier
- Black Formatter
- Solidity

### クローン

```
$ git clone https://github.com/M1n01/ft_transcendence.git
```

### 各環境の立ち上げ

```
# 環境変数ファイルの作成
$ cp .env.sample .env

# パッケージのインストール
$ npm install

# pre-commitの設定
$ pip install pre-commit
$ pre-commit install


# 環境の選択（以下のいずれかを実行）
$ make up   # ローカル環境
$ make dev  # dev環境
$ make      # 本番環境
```

### アクセス方法
```
https://localhost:3000/ # ローカル環境
https://localhost:8001/ # dev環境
https://localhost:8000/ # 本番環境
```

<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構造

```

```

<p align="right">(<a href="#top">トップへ</a>)</p>

## Gitの運用

### ブランチについて

mainとfeatureブランチで運用する。

| ブランチ名 |   役割   | 派生元 | マージ先 |
| :--------: | :------: | :----: | :------: |
|    main    | 本番環境 |   -    |    -     |
| feature/\* | 機能開発 |  main  |   main   |

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

<p align="right">(<a href="#top">トップへ</a>)</p>
