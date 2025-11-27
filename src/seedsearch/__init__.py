"""SeedSearch - 福岡工業大学の研究シーズ検索ツール"""

from .cli import cli

def main() -> None:
    """メインエントリーポイント"""
    cli()

__all__ = ["main", "cli"]
