import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_clean_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        print(f"Cleaned dataset loaded successfully: {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "ORDERDATE" in df.columns:
        df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")

    return df


def analyze_sales(df: pd.DataFrame):
    total_sales = df["SALES"].sum()
    average_sales = df["SALES"].mean()
    max_sales = df["SALES"].max()

    print("\n========== SALES SUMMARY ==========")
    print(f"Total Sales: {total_sales:,.2f}")
    print(f"Average Sales: {average_sales:,.2f}")
    print(f"Maximum Sale: {max_sales:,.2f}")

    sales_by_product = (
        df.groupby("PRODUCTLINE")["SALES"]
        .sum()
        .sort_values(ascending=False)
    )

    sales_by_country = (
        df.groupby("COUNTRY")["SALES"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    monthly_sales = (
        df.dropna(subset=["ORDERDATE"])
        .groupby(df["ORDERDATE"].dt.to_period("M"))["SALES"]
        .sum()
    )
    monthly_sales.index = monthly_sales.index.astype(str)

    return sales_by_product, sales_by_country, monthly_sales


def add_value_labels(ax, is_currency: bool = True):
    for container in ax.containers:
        labels = []
        for value in container.datavalues:
            if is_currency:
                labels.append(f"{value:,.0f}")
            else:
                labels.append(f"{value:.0f}")
        ax.bar_label(container, labels=labels, padding=3, fontsize=9)


def create_visualizations(
    sales_by_product: pd.Series,
    sales_by_country: pd.Series,
    monthly_sales: pd.Series
) -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.figsize": (11, 6)
    })

    # 1) Sales by Product Line
    fig, ax = plt.subplots()
    sales_by_product.plot(kind="bar", ax=ax)
    ax.set_title("Total Sales by Product Line", pad=15, weight="bold")
    ax.set_xlabel("Product Line")
    ax.set_ylabel("Sales")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30, ha="right")
    add_value_labels(ax)
    plt.tight_layout()
    plt.savefig(output_dir / "sales_by_product_line.png", dpi=300, bbox_inches="tight")
    plt.show()

    # 2) Top 10 Countries by Sales
    fig, ax = plt.subplots()
    sales_by_country.sort_values().plot(kind="barh", ax=ax)
    ax.set_title("Top 10 Countries by Sales", pad=15, weight="bold")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Country")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    add_value_labels(ax)
    plt.tight_layout()
    plt.savefig(output_dir / "top_10_countries_by_sales.png", dpi=300, bbox_inches="tight")
    plt.show()

    # 3) Monthly Sales Trend
    fig, ax = plt.subplots()
    monthly_sales.plot(kind="line", marker="o", ax=ax)
    ax.set_title("Monthly Sales Trend", pad=15, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="both", linestyle="--", alpha=0.4)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_sales_trend.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("\nProfessional charts saved successfully in the output folder.")


def main():
    input_file = "output/cleaned_sales_data.csv"

    df = load_clean_data(input_file)
    df = prepare_data(df)

    sales_by_product, sales_by_country, monthly_sales = analyze_sales(df)
    create_visualizations(sales_by_product, sales_by_country, monthly_sales)


if __name__ == "__main__":
    main()