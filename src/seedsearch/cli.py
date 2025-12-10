"""CLIエントリーポイント"""

import click
from pathlib import Path

from .loader import DataLoader
from .search import ResearchSearcher
from .display import ResultDisplay


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """福岡工業大学の研究シーズ検索ツール"""
    pass


@cli.command()
@click.argument("query")
@click.option(
    "--exact", "-e",
    is_flag=True,
    help="完全一致検索（デフォルトは部分一致）"
)
@click.option(
    "--field", "-f",
    type=click.Choice(["all", "title", "keyword", "overview", "researcher"]),
    default="all",
    help="検索対象フィールド"
)
@click.option(
    "--operator", "-op",
    type=click.Choice(["and", "or"]),
    default="and",
    help="複数ワードの検索方法（and: すべて含む / or: いずれか含む、デフォルトはand）"
)
@click.option(
    "--limit", "-l",
    type=int,
    default=None,
    help="表示件数の制限"
)
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="出力形式（table/json/csv）"
)
def search(query: str, exact: bool, field: str, operator: str, limit: int, output: str):
    """研究シーズを検索

    \b
    例:
      seedsearch search "AI"
      seedsearch search "AI ロボット"              # AND検索（両方含む）
      seedsearch search "AI ロボット" --operator or  # OR検索（いずれか含む）
      seedsearch search "ロボット" --field keyword
      seedsearch search "松尾" --field researcher --limit 10
    """
    try:
        # データを読み込み
        loader = DataLoader()
        data = loader.load()

        # 検索を実行
        searcher = ResearchSearcher(data)
        results = searcher.search(query, exact=exact, field=field, operator=operator)

        # limit適用
        if limit:
            results = results.head(limit)

        # 結果を表示
        display = ResultDisplay()
        if output == "json":
            display.output_json(results)
        elif output == "csv":
            display.output_csv(results)
        else:  # table
            # 複数ワード検索の場合、キーワードをリスト化してハイライト
            search_keywords = [kw.strip() for kw in query.split() if kw.strip()]
            display.display_list(results, limit=limit, search_keywords=search_keywords)
            # サマリーも表示
            if not results.empty and len(results) > 5:
                display.display_summary(results)

    except FileNotFoundError as e:
        click.echo(f"エラー: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"エラーが発生しました: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("research_id")
def show(research_id: str):
    """研究課題の詳細を表示

    \b
    例:
      seedsearch show 25KJ2239
    """
    try:
        # データを読み込み
        loader = DataLoader()
        data = loader.load()

        # 研究課題を取得
        searcher = ResearchSearcher(data)
        result = searcher.get_by_id(research_id)

        if result is None:
            click.echo(f"\n研究課題が見つかりませんでした: {research_id}\n")
            return

        # 詳細を表示
        display = ResultDisplay()
        display.display_detail(result)

    except FileNotFoundError as e:
        click.echo(f"エラー: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"エラーが発生しました: {e}", err=True)
        raise click.Abort()


@cli.command()
def info():
    """データファイルの情報を表示"""
    try:
        loader = DataLoader()
        data = loader.load()

        click.echo(f"\nデータファイル: {loader.csv_path}")
        click.echo(f"総研究課題数: {len(data)}件")
        click.echo(f"列数: {len(data.columns)}列\n")

        if "研究種目" in data.columns:
            click.echo("【研究種目別の内訳】")
            type_counts = data["研究種目"].value_counts()
            for research_type, count in type_counts.head(10).items():
                click.echo(f"  {research_type}: {count}件")
            click.echo()

    except FileNotFoundError as e:
        click.echo(f"エラー: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"エラーが発生しました: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
