"""検索結果の表示"""

import pandas as pd
import re
from typing import Optional, List, Union


class ResultDisplay:
    """検索結果を表示するクラス"""

    @staticmethod
    def _highlight_keywords(text: str, keywords: Union[str, List[str], None]) -> str:
        """
        テキスト中のキーワードをハイライト表示

        Args:
            text: ハイライト対象のテキスト
            keywords: ハイライトするキーワード（文字列またはリスト）

        Returns:
            ハイライトされたテキスト
        """
        if not keywords or not text:
            return text

        # キーワードをリストに変換
        if isinstance(keywords, str):
            keyword_list = [keywords]
        else:
            keyword_list = keywords

        # ANSIカラーコード（黄色でハイライト）
        HIGHLIGHT = "\033[93m"  # 明るい黄色
        RESET = "\033[0m"

        highlighted_text = text
        for keyword in keyword_list:
            if keyword:
                # 大文字小文字を区別しない検索と置換
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                highlighted_text = pattern.sub(
                    lambda m: f"{HIGHLIGHT}{m.group()}{RESET}",
                    highlighted_text
                )

        return highlighted_text

    @staticmethod
    def display_list(
        results: pd.DataFrame,
        limit: Optional[int] = None,
        search_keywords: Union[str, List[str], None] = None
    ) -> None:
        """
        検索結果をリスト形式で表示

        Args:
            results: 検索結果のDataFrame
            limit: 表示する最大件数（Noneの場合は全件表示）
            search_keywords: ハイライトする検索キーワード（文字列またはリスト）
        """
        if results.empty:
            print("\n検索結果が見つかりませんでした")
            print("→ 検索ワードを変更してみてください\n")
            return

        total_count = len(results)
        display_count = min(total_count, limit) if limit else total_count

        print(f"\n検索結果: {total_count}件")
        if limit and total_count > limit:
            print(f"(最初の{limit}件を表示)")
        print()

        for idx, (_, row) in enumerate(results.head(display_count).iterrows(), 1):
            # 研究課題番号
            research_id = row.get("研究課題/領域番号", "N/A")

            # 研究課題名
            title = row.get("研究課題名", "タイトルなし")
            title = ResultDisplay._highlight_keywords(title, search_keywords)

            # 研究代表者（所属も含む）
            researcher = row.get("研究代表者", "不明")
            researcher = ResultDisplay._highlight_keywords(researcher, search_keywords)

            # 研究分担者
            co_investigators = row.get("研究分担者", "")
            co_investigators_display = ""
            if pd.notna(co_investigators) and co_investigators:
                # 改行で分割して最初の2名まで表示
                co_inv_list = str(co_investigators).split("\n")[:2]
                co_investigators_display = ", \n               ".join([name.strip() for name in co_inv_list if name.strip()])
                co_investigators_display = ResultDisplay._highlight_keywords(co_investigators_display, search_keywords)
                # if len(str(co_investigators).split("\n")) > 2:
                #     co_investigators_display += " 他"

            # キーワード
            keywords = row.get("キーワード", "")
            if pd.notna(keywords) and keywords:
                # キーワードが長すぎる場合は最初の3つまで
                keyword_list = str(keywords).split(" / ")[:3]
                keywords_display = ", ".join(keyword_list)
                if len(str(keywords).split(" / ")) > 3:
                    keywords_display += "..."
                keywords_display = ResultDisplay._highlight_keywords(keywords_display, search_keywords)
            else:
                keywords_display = "なし"

            print(f"{idx}. [{research_id}] {title}")
            print(f"   研究代表者: {researcher}")
            if co_investigators_display:
                print(f"   研究分担者: {co_investigators_display}")
            print(f"   キーワード: {keywords_display}")
            print()

    @staticmethod
    def display_detail(
        row: pd.Series,
        search_keywords: Union[str, List[str], None] = None
    ) -> None:
        """
        研究課題の詳細を表示

        Args:
            row: 研究課題データ（pandas Series）
            search_keywords: ハイライトする検索キーワード（文字列またはリスト）
        """
        print("\n" + "=" * 80)
        print("研究課題詳細")
        print("=" * 80)

        # 主要フィールドを表示
        fields = [
            ("研究課題/領域番号", "研究課題番号"),
            ("研究課題名", "研究課題名"),
            ("研究課題名 (英文)", "研究課題名（英文）"),
            ("研究代表者", "研究代表者"),
            ("研究分担者", "研究分担者"),
            ("研究期間 (年度)", "研究期間"),
            ("研究種目", "研究種目"),
            ("研究分野", "研究分野"),
            ("審査区分", "審査区分"),
            ("キーワード", "キーワード"),
            ("総配分額", "総配分額"),
            ("研究開始時の研究の概要", "研究開始時の概要"),
            ("研究概要", "研究概要"),
            ("研究概要 (英文)", "研究概要（英文）"),
        ]

        for csv_field, display_name in fields:
            value = row.get(csv_field, "")
            if pd.notna(value) and value != "":
                # 検索キーワードをハイライト
                highlighted_value = ResultDisplay._highlight_keywords(str(value), search_keywords)
                print(f"\n【{display_name}】")
                print(f"{highlighted_value}")

        print("\n" + "=" * 80 + "\n")

    @staticmethod
    def display_summary(results: pd.DataFrame) -> None:
        """
        検索結果のサマリーを表示

        Args:
            results: 検索結果のDataFrame
        """
        total = len(results)
        print(f"\n検索結果: {total}件\n")

        if total > 0 and "研究種目" in results.columns:
            print("【研究種目別の内訳】")
            type_counts = results["研究種目"].value_counts()
            for research_type, count in type_counts.items():
                if pd.notna(research_type):
                    print(f"  {research_type}: {count}件")
            print()
