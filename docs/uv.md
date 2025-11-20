# uvのセットアップ手順

## uvとは

uvは、Rustで書かれた高速なPythonパッケージマネージャーです。以下の機能を提供します：

- **仮想環境の管理**: `venv` の代替
- **依存関係の管理**: `pip` の代替
- **Pythonバージョン管理**: `pyenv` の代替
- **プロジェクト管理**: `poetry` や `pipenv` の代替

従来のツールと比較して、10〜100倍高速に動作します。

## 前提条件

このプロジェクトでは **Python 3.11以上** が必要です。

---

## Windows でのセットアップ

### 1. uvのインストール

#### PowerShell を使用する方法（推奨）

PowerShellを管理者権限で開き、以下のコマンドを実行します：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Scoop を使用する方法

Scoopがインストールされている場合：

```powershell
scoop install uv
```

#### winget を使用する方法

```powershell
winget install --id=astral-sh.uv -e
```

### 2. インストールの確認

```powershell
uv --version
```

バージョンが表示されれば、インストール成功です。

### 3. PATHの設定（必要な場合）

通常は自動的に設定されますが、コマンドが認識されない場合は、以下のパスを環境変数PATHに追加してください：

```
%USERPROFILE%\.cargo\bin
```

**設定方法：**
1. 「システムのプロパティ」→「環境変数」を開く
2. ユーザー環境変数の「Path」を選択して編集
3. 上記のパスを追加
4. PowerShellを再起動

---

## Mac でのセットアップ

### 1. uvのインストール

#### curl を使用する方法（推奨）

ターミナルを開き、以下のコマンドを実行します：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Homebrew を使用する方法

Homebrewがインストールされている場合：

```bash
brew install uv
```

### 2. インストールの確認

```bash
uv --version
```

バージョンが表示されれば、インストール成功です。

### 3. シェルの設定（curl でインストールした場合）

インストール後、シェル設定ファイルを再読み込みします：

**bashの場合：**
```bash
source ~/.bashrc
```

**zshの場合：**
```bash
source ~/.zshrc
```

---

## プロジェクトのセットアップ

### 1. リポジトリのクローン

```bash
git clone <リポジトリURL>
cd SeedSearch
```

### 2. Python バージョンの確認

プロジェクトに `.python-version` ファイルがあるため、uvが自動的に適切なPythonバージョンを検出します。

現在のPythonバージョンを確認：

```bash
uv python list
```

必要に応じてPython 3.11以上をインストール：

```bash
uv python install 3.11
```

### 3. 仮想環境の作成

```bash
uv venv
```

このコマンドで `.venv` ディレクトリに仮想環境が作成されます。

### 4. 仮想環境の有効化（任意）

uvは自動的に仮想環境を使用するため、通常は有効化不要ですが、手動で有効化する場合：

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 5. 依存関係のインストール

```bash
uv sync
```

または

```bash
uv pip install -e .
```

### 6. プロジェクトの実行

```bash
uv run seedsearch <検索ワード>
```

---

## よく使うuvコマンド

### プロジェクト管理

| コマンド | 説明 |
|---------|------|
| `uv init` | 新しいプロジェクトを初期化 |
| `uv sync` | 依存関係を同期（ロックファイルに基づく） |
| `uv lock` | 依存関係をロックファイルに記録 |
| `uv run <コマンド>` | 仮想環境でコマンドを実行 |

### パッケージ管理

| コマンド | 説明 |
|---------|------|
| `uv add <パッケージ>` | パッケージを追加 |
| `uv remove <パッケージ>` | パッケージを削除 |
| `uv pip install <パッケージ>` | パッケージをインストール（pip互換） |
| `uv pip list` | インストール済みパッケージの一覧 |
| `uv pip freeze` | 依存関係を出力 |

### Python バージョン管理

| コマンド | 説明 |
|---------|------|
| `uv python list` | 利用可能なPythonバージョンを表示 |
| `uv python install <バージョン>` | Pythonバージョンをインストール |
| `uv python pin <バージョン>` | プロジェクトのPythonバージョンを固定 |

### 仮想環境管理

| コマンド | 説明 |
|---------|------|
| `uv venv` | 仮想環境を作成 |
| `uv venv --python 3.11` | 特定のバージョンで仮想環境を作成 |
| `uv venv .venv` | 指定したディレクトリに仮想環境を作成 |

### ツール管理

| コマンド | 説明 |
|---------|------|
| `uv tool install <ツール>` | グローバルツールをインストール |
| `uv tool run <ツール>` | ツールを一時的に実行 |
| `uvx <ツール>` | ツールを一時実行（エイリアス） |

---

## 開発ワークフロー例

### 新しい依存関係を追加する

```bash
# パッケージを追加
uv add requests

# 開発用の依存関係を追加
uv add --dev pytest
```

### アプリケーションを実行する

```bash
# プロジェクトのコマンドを実行
uv run seedsearch "研究テーマ"

# Pythonスクリプトを実行
uv run python main.py
```

### テストを実行する

```bash
uv run pytest
```

### 依存関係を更新する

```bash
# すべての依存関係を最新に更新
uv lock --upgrade

# 特定のパッケージのみ更新
uv lock --upgrade-package requests
```

---

## トラブルシューティング

### コマンドが認識されない（Windows）

**原因**: PATHが設定されていない

**解決策**:
1. PowerShellを再起動
2. 環境変数PATHに `%USERPROFILE%\.cargo\bin` を追加
3. システムを再起動

### コマンドが認識されない（Mac）

**原因**: シェル設定が読み込まれていない

**解決策**:
```bash
source ~/.zshrc  # または ~/.bashrc
```

### Python バージョンが見つからない

**解決策**:
```bash
# Pythonをuvでインストール
uv python install 3.11
```

### 依存関係のインストールに失敗する

**解決策**:
```bash
# キャッシュをクリア
uv cache clean

# 再度インストール
uv sync
```

### 仮想環境が壊れた場合

**解決策**:
```bash
# 仮想環境を削除
rm -rf .venv  # Mac/Linux
rmdir /s .venv  # Windows

# 再作成
uv venv
uv sync
```

---

## 参考資料

- [uv公式ドキュメント](https://docs.astral.sh/uv/)
- [Pythonパッケージ管理 [uv] 完全入門](https://speakerdeck.com/mickey_kubo/pythonpatukeziguan-li-uv-wan-quan-ru-men)
- [技術評論社の記事](https://gihyo.jp/article/2024/09/monthly-python-2409)

---

## その他の便利なコマンド

### プロジェクト情報の表示

```bash
# pyproject.tomlの内容を確認
cat pyproject.toml

# ロックファイルの内容を確認
cat uv.lock
```

### 環境変数の確認

**Windows:**
```powershell
$env:PATH
```

**Mac/Linux:**
```bash
echo $PATH
```

### uvの更新

```bash
# 自分自身を更新
uv self update
```
