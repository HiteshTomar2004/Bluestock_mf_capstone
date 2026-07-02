import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

scorecard = pd.read_csv(
    BASE_DIR / "data" / "analytics" / "fund_scorecard.csv"
)

scheme = pd.read_csv(
    BASE_DIR / "data" / "processed" / "clean_scheme_performance.csv"
)

funds = scorecard.merge(
    scheme[
        [
            "amfi_code",
            "risk_grade"
        ]
    ],
    on="amfi_code",
    how="left"
)
def recommend_funds(risk_appetite):

    mapping = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"]
    }

    if risk_appetite not in mapping:
        print("Choose Low, Moderate or High.")
        return

    recommendations = (
        funds[
            funds["risk_grade"].isin(mapping[risk_appetite])
        ]
        .sort_values(
            "sharpe_ratio",
            ascending=False
        )
        .head(3)
    )

    print("\nTop 3 Recommended Funds\n")

    print(
        recommendations[
            [
                "scheme_name",
                "risk_grade",
                "sharpe_ratio",
                "fund_score"
            ]
        ]
    )


recommend_funds("Low")
recommend_funds("Moderate")
recommend_funds("High")