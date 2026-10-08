from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
CLIENTS_COUNT = 1500

np.random.seed(RANDOM_SEED)


def generate_clients(count: int) -> pd.DataFrame:
    industries = [
        "IT",
        "Retail",
        "Construction",
        "Logistics",
        "Healthcare",
        "Education",
        "Professional Services",
    ]

    company_ids = np.arange(1, count + 1)

    industry = np.random.choice(
        industries,
        size=count,
        p=[0.18, 0.22, 0.14, 0.12, 0.10, 0.08, 0.16],
    )

    employees = np.random.randint(1, 250, size=count)

    turnover = np.random.lognormal(
        mean=15,
        sigma=1.2,
        size=count,
    ).astype(int)

    transactions = np.maximum(
        1,
        (
            turnover / 120_000
            + employees * 0.7
            + np.random.normal(0, 20, count)
        ).astype(int),
    )

    tariff = np.select(
        [
            turnover < 3_000_000,
            turnover < 15_000_000,
        ],
        [
            "Start",
            "Business",
        ],
        default="Premium",
    )

    has_card = np.random.rand(count) < np.clip(
        0.35 + transactions / 600,
        0.35,
        0.90,
    )

    retail_mask = industry == "Retail"

    acquiring_probability = np.where(
        retail_mask,
        0.78,
        0.25,
    )

    has_acquiring = np.random.rand(count) < acquiring_probability

    salary_probability = np.clip(
        employees / 120,
        0.10,
        0.85,
    )

    has_salary_project = np.random.rand(count) < salary_probability

    support_requests = np.random.poisson(
        lam=1.3,
        size=count,
    )

    product_count = (
        has_card.astype(int)
        + has_acquiring.astype(int)
        + has_salary_project.astype(int)
    )

    revenue = (
        800
        + transactions * 18
        + has_card * 450
        + has_acquiring * 1100
        + has_salary_project * 900
        + product_count * 300
    )

    revenue = (
        revenue
        + np.random.normal(0, 500, count)
    ).clip(min=200).astype(int)

    churn_probability = (
        0.04
        + support_requests * 0.025
        - product_count * 0.015
    )

    churn_probability = np.clip(
        churn_probability,
        0.02,
        0.45,
    )

    churned = np.random.rand(count) < churn_probability

    return pd.DataFrame(
        {
            "company_id": company_ids,
            "industry": industry,
            "employees": employees,
            "turnover": turnover,
            "tariff": tariff,
            "transactions": transactions,
            "revenue": revenue,
            "has_card": has_card,
            "has_acquiring": has_acquiring,
            "has_salary_project": has_salary_project,
            "support_requests": support_requests,
            "churned": churned,
        }
    )


def main():
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(exist_ok=True)

    df = generate_clients(CLIENTS_COUNT)

    output_path = data_dir / "companies.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} clients")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
