import pandas as pd


def add_basic_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exemplo de transformações adicionais:
    - precisão de passe
    - razão remates à baliza / remates totais
    """
    df = df.copy()

    if "passes_completed_home" in df and "passes_total_home" in df:
        df["pass_accuracy_home"] = df["passes_completed_home"] / df["passes_total_home"].replace(0, 1)
    if "passes_completed_away" in df and "passes_total_away" in df:
        df["pass_accuracy_away"] = df["passes_completed_away"] / df["passes_total_away"].replace(0, 1)

    if "shots_on_target_home" in df and "shots_home" in df:
        df["shots_on_target_ratio_home"] = df["shots_on_target_home"] / df["shots_home"].replace(0, 1)
    if "shots_on_target_away" in df and "shots_away" in df:
        df["shots_on_target_ratio_away"] = df["shots_on_target_away"] / df["shots_away"].replace(0, 1)

    return df
