"""科研費データの前処理スクリプト

このスクリプトは以下の前処理を実行します:
1. BOMの除去
2. 必要な列の抽出
3. テキストのクリーニング
4. 欠損値の処理
5. クリーニング済みデータの保存
"""

import pandas as pd
import re
from pathlib import Path


def clean_text(text: str) -> str:
    """テキストデータのクリーニング

    Args:
        text: クリーニング対象のテキスト

    Returns:
        クリーニング済みテキスト
    """
    if pd.isna(text) or text == "":
        return ""

    # 文字列に変換
    text = str(text)

    # 改行を空白に置換
    text = text.replace('\n', ' ').replace('\r', ' ')

    # 複数の空白を1つに
    text = re.sub(r'\s+', ' ', text)

    # 前後の空白を削除
    text = text.strip()

    return text


def preprocess_kaken_data(
    input_path: str | Path,
    output_path: str | Path,
    columns_to_extract: list[str] | None = None
) -> pd.DataFrame:
    """科研費データの前処理

    Args:
        input_path: 入力CSVファイルのパス
        output_path: 出力CSVファイルのパス
        columns_to_extract: 抽出する列名のリスト（Noneの場合はデフォルト列を使用）

    Returns:
        前処理済みのDataFrame
    """
    # デフォルトで抽出する列（ベクトル化に有用な列）
    if columns_to_extract is None:
        columns_to_extract = [
            "研究課題名",
            "研究課題名 (英文)",
            "研究課題/領域番号",
            "キーワード",
            "研究分野",
            "審査区分",
            "研究種目",
            "研究開始時の研究の概要",
            "研究概要",
            "研究成果の概要",
        ]

    # CSVを読み込み（BOMを自動処理）
    print(f"データを読み込み中: {input_path}")
    df = pd.read_csv(input_path, encoding='utf-8-sig')

    print(f"元のデータ: {len(df)} 行, {len(df.columns)} 列")

    # 指定された列のみを抽出
    available_columns = [col for col in columns_to_extract if col in df.columns]
    missing_columns = [col for col in columns_to_extract if col not in df.columns]

    if missing_columns:
        print(f"警告: 以下の列が見つかりませんでした: {missing_columns}")

    df_extracted = df[available_columns].copy()
    print(f"列を抽出: {len(available_columns)} 列")

    # テキスト列のクリーニング
    text_columns = [
        "研究課題名",
        "研究課題名 (英文)",
        "キーワード",
        "研究分野",
        "審査区分",
        "研究種目",
        "研究開始時の研究の概要",
        "研究概要",
        "研究成果の概要",
    ]

    print("テキストをクリーニング中...")
    for col in text_columns:
        if col in df_extracted.columns:
            df_extracted[col] = df_extracted[col].apply(clean_text)

    # 欠損値を空文字列で埋める
    df_extracted = df_extracted.fillna("")

    # 全ての列が空の行を削除
    df_extracted = df_extracted[df_extracted.astype(bool).any(axis=1)]

    print(f"前処理後のデータ: {len(df_extracted)} 行, {len(df_extracted.columns)} 列")

    # 結合テキスト列を作成（ベクトル化用）
    print("結合テキスト列を作成中...")
    df_extracted['combined_text'] = (
        df_extracted['研究課題名'] + ' ' +
        df_extracted.get('キーワード', '') + ' ' +
        df_extracted.get('研究概要', '') + ' ' +
        df_extracted.get('研究成果の概要', '')
    ).apply(clean_text)

    # クリーニング済みデータを保存
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"クリーニング済みデータを保存中: {output_path}")
    df_extracted.to_csv(output_path, index=False, encoding='utf-8-sig')

    print("前処理が完了しました!")

    # データの統計情報を表示
    print("\n=== データ統計 ===")
    print(f"総行数: {len(df_extracted)}")
    print(f"総列数: {len(df_extracted.columns)}")
    print(f"\n列名:")
    for i, col in enumerate(df_extracted.columns, 1):
        non_empty = (df_extracted[col] != "").sum()
        print(f"  {i}. {col}: {non_empty}/{len(df_extracted)} 件")

    return df_extracted


def main():
    """メイン処理"""
    # プロジェクトルートからの相対パス
    project_root = Path(__file__).parent.parent.parent
    input_path = project_root / "data" / "kaken.csv"
    output_path = project_root / "data" / "kaken_cleaned.csv"

    # 前処理を実行
    df = preprocess_kaken_data(input_path, output_path)

    # サンプルデータを表示
    print("\n=== サンプルデータ（最初の3行） ===")
    print(df.head(3)[['研究課題名', 'キーワード', 'combined_text']].to_string())


if __name__ == "__main__":
    main()