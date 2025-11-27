"""データモデル定義"""

from typing import TypedDict, Optional


class ResearchProject(TypedDict):
    """研究課題のデータモデル"""

    # 基本情報
    research_id: str  # 研究課題/領域番号
    title: str  # 研究課題名
    title_en: Optional[str]  # 研究課題名（英文）

    # 研究者情報
    principal_investigator: str  # 研究代表者
    co_investigators: Optional[str]  # 研究分担者

    # 研究内容
    keywords: Optional[str]  # キーワード
    research_field: Optional[str]  # 研究分野
    research_category: Optional[str]  # 審査区分
    research_type: Optional[str]  # 研究種目

    # 期間・予算
    research_period: Optional[str]  # 研究期間
    total_budget: Optional[str]  # 総配分額

    # 研究概要
    initial_overview: Optional[str]  # 研究開始時の研究の概要
    overview: Optional[str]  # 研究概要
    overview_en: Optional[str]  # 研究概要（英文）

    # 所属機関
    institution: Optional[str]  # 研究機関
