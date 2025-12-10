# Seed Search

福岡工業大学が持つ研究シーズを検索するシステム

> 「研究シーズ」とは、将来的に製品やサービスに発展する可能性を秘めた「技術の種」のこと

## 使用技術

- python

Python のパッケージマネージャーである『uv』を使用して、仮想環境・依存関係・バージョン管理を行う
以下の記事を参考にする
[Python パッケージ管理 [uv] 完全入門](https://speakerdeck.com/mickey_kubo/pythonpatukeziguan-li-uv-wan-quan-ru-men)
https://gihyo.jp/article/2024/09/monthly-python-2409

## 使い方

```bash
seedsearch search <検索ワード>
seedsearch show <研究課題ID>
```

## データソース

本プロジェクトで使用している研究データは、以下のデータベースから取得しています：

**出典：KAKEN：科学研究費助成事業データベース（国立情報学研究所）**
https://kaken.nii.ac.jp/

- **ライセンス**: [クリエイティブ・コモンズ表示 4.0 国際（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.ja)
- データは加工して使用しています（`kaken_cleaned.csv`）
- データの詳細とライセンス情報については [data/README.md](data/README.md) を参照してください

## 導入方法

1. 事前環境を整える
   [環境構築](docs/introduce_features.md)を参照してください

2. ターミナルで使用する
   グローバルインストールの場合

```bash
seedsearch --help
```

ローカルインストールの場合

```bash
uv run seedsearch --help
```

詳細は [docs/introduce_features.md](docs/introduce_features.md) を参照してください

## 開発者用 開発環境構築手順

1. リポジトリをクローンする

```bash
git clone git@github.com:KOU050223/SeedSearch.git
cd SeedSearch/
```

2. 依存関係をインストールする

```bash
uv sync
```

3. happy hacking!

## 将来の展望

- DB を外部 DB にすることにより DB セットアップなしで一般的な CLI アプリケーションとして利用できるようにする
- 作成したツール（パッケージ）を PyPI に公開し、pip でインストールできるようにする
- Web アプリケーション化
