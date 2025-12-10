"""検索ロジック"""

import pandas as pd
from typing import Optional


class ResearchSearcher:
    """研究課題の検索を行うクラス"""

    # 検索対象のフィールド名（KAKENのCSV列名）
    SEARCH_FIELDS = {
        "all": [
            "研究課題名",
            "研究課題名 (英文)",
            "キーワード",
            "研究概要",
            "研究概要 (英文)",
            "研究代表者",
            "研究分担者",
            "研究分野",
        ],
        "title": ["研究課題名", "研究課題名 (英文)"],
        "keyword": ["キーワード"],
        "overview": ["研究概要", "研究概要 (英文)", "研究開始時の研究の概要"],
        "researcher": ["研究代表者", "研究分担者"],
    }

    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data: 検索対象のDataFrame
        """
        self.data = data

    def search(
        self,
        query: str,
        exact: bool = False,
        field: str = "all",
        operator: str = "and",
    ) -> pd.DataFrame:
        """
        キーワードで研究課題を検索（複数ワード対応）

        Args:
            query: 検索キーワード（スペース区切りで複数指定可能）
            exact: True の場合は完全一致検索、False の場合は部分一致検索
            field: 検索対象フィールド（"all", "title", "keyword", "overview", "researcher"）
            operator: 複数キーワードの結合方法（"and" または "or"、デフォルトは "and"）

        Returns:
            pd.DataFrame: 検索結果

        Raises:
            ValueError: 無効なfieldまたはoperatorが指定された場合
        """
        if field not in self.SEARCH_FIELDS:
            raise ValueError(
                f"無効な検索フィールドです: {field}\n"
                f"使用可能なフィールド: {', '.join(self.SEARCH_FIELDS.keys())}"
            )

        if operator not in ["and", "or"]:
            raise ValueError(
                f"無効な演算子です: {operator}\n"
                f"使用可能な演算子: 'and', 'or'"
            )

        target_columns = self.SEARCH_FIELDS[field]

        # 検索対象の列が存在するか確認
        existing_columns = [col for col in target_columns if col in self.data.columns]

        if not existing_columns:
            raise ValueError(
                f"検索対象の列が見つかりません。\n"
                f"期待される列: {target_columns}"
            )

        # 検索クエリを複数ワードに分割（スペース区切り）
        keywords = [kw.strip() for kw in query.split() if kw.strip()]

        if not keywords:
            # 空の検索クエリの場合は空のDataFrameを返す
            return self.data.iloc[0:0]

        # 複数キーワードのAND/OR検索
        if operator == "and":
            # AND検索: すべてのキーワードを含む行のみ
            mask = pd.Series([True] * len(self.data), index=self.data.index)

            for keyword in keywords:
                keyword_mask = pd.Series([False] * len(self.data), index=self.data.index)

                for col in existing_columns:
                    if exact:
                        # 完全一致検索
                        keyword_mask |= self.data[col].astype(str) == keyword
                    else:
                        # 部分一致検索（大文字小文字を区別しない）
                        keyword_mask |= self.data[col].astype(str).str.contains(
                            keyword, case=False, na=False, regex=False
                        )

                # すべてのキーワードを含む必要があるのでAND結合
                mask &= keyword_mask
        else:
            # OR検索: いずれかのキーワードを含む行
            mask = pd.Series([False] * len(self.data), index=self.data.index)

            for keyword in keywords:
                keyword_mask = pd.Series([False] * len(self.data), index=self.data.index)

                for col in existing_columns:
                    if exact:
                        # 完全一致検索
                        keyword_mask |= self.data[col].astype(str) == keyword
                    else:
                        # 部分一致検索（大文字小文字を区別しない）
                        keyword_mask |= self.data[col].astype(str).str.contains(
                            keyword, case=False, na=False, regex=False
                        )

                # いずれかのキーワードにヒットしたらOR結合
                mask |= keyword_mask

        return self.data[mask]

    def get_by_id(self, research_id: str) -> Optional[pd.Series]:
        """
        研究課題番号で特定の研究課題を取得

        Args:
            research_id: 研究課題/領域番号

        Returns:
            pd.Series: 研究課題データ、見つからない場合はNone
        """
        if "研究課題/領域番号" not in self.data.columns:
            raise ValueError("研究課題/領域番号の列が見つかりません")

        result = self.data[self.data["研究課題/領域番号"] == research_id]

        if result.empty:
            return None

        return result.iloc[0]
