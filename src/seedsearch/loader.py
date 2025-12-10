"""CSVデータローダー"""

import pandas as pd
from pathlib import Path
from typing import Optional
from importlib.resources import files


class DataLoader:
    """KAKENのCSVデータを読み込むクラス"""

    def __init__(self, csv_path: Optional[Path] = None):
        """
        Args:
            csv_path: CSVファイルのパス。Noneの場合はデフォルトパスを使用
        """
        if csv_path is None:
            # パッケージ内のデータファイルを使用
            data_file = files("seedsearch.data").joinpath("kaken.csv")
            self.csv_path = Path(str(data_file))
        else:
            self.csv_path = csv_path

    def load(self) -> pd.DataFrame:
        """
        CSVファイルを読み込んでDataFrameを返す

        Returns:
            pd.DataFrame: 研究課題データ

        Raises:
            FileNotFoundError: CSVファイルが見つからない場合
            pd.errors.EmptyDataError: CSVファイルが空の場合
        """
        try:
            # CSVを読み込み（BOM付きUTF-8に対応）
            # パッケージ内のリソースの場合は直接読み込み
            from importlib.resources import as_file

            # csv_pathがパッケージリソースかどうかを確認
            if "seedsearch" in str(self.csv_path) and not self.csv_path.exists():
                # パッケージリソースから読み込み
                data_file = files("seedsearch.data").joinpath("kaken.csv")
                with as_file(data_file) as csv_file:
                    df = pd.read_csv(csv_file, encoding="utf-8-sig")
            else:
                # 通常のファイルパスから読み込み
                if not self.csv_path.exists():
                    raise FileNotFoundError(
                        f"データファイルが見つかりません: {self.csv_path}\n"
                        f"data/kaken.csv を配置してください"
                    )
                df = pd.read_csv(self.csv_path, encoding="utf-8-sig")

            if df.empty:
                raise pd.errors.EmptyDataError("CSVファイルにデータがありません")

            return df

        except pd.errors.EmptyDataError as e:
            raise pd.errors.EmptyDataError(
                f"CSVファイルが空です: {self.csv_path}"
            ) from e
        except FileNotFoundError:
            raise
        except Exception as e:
            raise Exception(
                f"CSVファイルの読み込みに失敗しました: {self.csv_path}\n"
                f"エラー: {str(e)}"
            ) from e

    def get_column_names(self) -> list[str]:
        """
        CSVファイルの列名を取得

        Returns:
            list[str]: 列名のリスト
        """
        df = self.load()
        return df.columns.tolist()
