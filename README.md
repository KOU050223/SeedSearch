# Seed Search
福岡工業大学が持つ研究シーズを検索するシステム

> 「研究シーズ」とは、将来的に製品やサービスに発展する可能性を秘めた「技術の種」のこと

## 使用技術

- python

Pythonのパッケージマネージャーである『uv』を使用して、仮想環境・依存関係・バージョン管理を行う
以下の記事を参考にする
[Pythonパッケージ管理 [uv] 完全入門](https://speakerdeck.com/mickey_kubo/pythonpatukeziguan-li-uv-wan-quan-ru-men)
https://gihyo.jp/article/2024/09/monthly-python-2409

## uvセットアップ
[uvのセットアップ手順](docs/uv.md)

## 使い方
1. uvのセットアップ手順に従い、開発環境を構築する
2. データベースをセットアップする
3. 以下のコマンドを実行し、検索ワードを引数に渡す
```bash
uv run seedsearch <検索ワード>
```

## データソース

本プロジェクトで使用している研究データは、以下のデータベースから取得しています：

**出典：KAKEN：科学研究費助成事業データベース（国立情報学研究所）**
https://kaken.nii.ac.jp/

- **ライセンス**: [クリエイティブ・コモンズ表示4.0国際（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.ja)
- データは加工して使用しています（`kaken_cleaned.csv`）
- データの詳細とライセンス情報については [data/README.md](data/README.md) を参照してください

## 開発環境構築手順
1. リポジトリをクローンする
2. uvをインストールする
3. uvで仮想環境を構築する
```bash
uv venv
```
4. 依存関係をインストールする
```bash
uv install
```
5. happy hacking!

## 将来の展望
- DBを外部DBにすることによりDBセットアップなしで一般的なCLIアプリケーションとして利用できるようにする
- 作成したツール（パッケージ）をPyPIに公開し、pipでインストールできるようにする
- Gitレポジトリを公開すればそこからインストールできるようにする
- Webアプリケーション化
