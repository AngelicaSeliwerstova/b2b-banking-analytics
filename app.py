import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="B2B Banking Analytics",
    layout="wide"
)


df = pd.read_csv("data/companies.csv")


st.title("B2B Banking Analytics")
st.write("Анализ клиентов и банковских продуктов для малого и среднего бизнеса.")


industries = st.multiselect(
    "Отрасль",
    df["industry"].unique(),
    default=df["industry"].unique()
)

filtered = df[df["industry"].isin(industries)]


clients = len(filtered)
revenue = filtered["revenue"].sum()
avg_revenue = filtered["revenue"].mean()
churn_rate = filtered["churned"].mean() * 100


col1, col2, col3, col4 = st.columns(4)

col1.metric("Клиенты", clients)
col2.metric("Выручка", f"{revenue:,.0f} ₽")
col3.metric("Средняя выручка", f"{avg_revenue:,.0f} ₽")
col4.metric("Отток", f"{churn_rate:.1f}%")


st.subheader("Выручка по отраслям")

revenue_by_industry = (
    filtered
    .groupby("industry", as_index=False)["revenue"]
    .sum()
)

fig = px.bar(
    revenue_by_industry,
    x="industry",
    y="revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Использование продуктов")

products = pd.DataFrame({
    "Продукт": [
        "Бизнес-карта",
        "Эквайринг",
        "Зарплатный проект"
    ],
    "Клиенты": [
        filtered["has_card"].sum(),
        filtered["has_acquiring"].sum(),
        filtered["has_salary_project"].sum()
    ]
})

fig = px.bar(
    products,
    x="Продукт",
    y="Клиенты"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Что можно заметить")


card_clients = filtered[
    (filtered["transactions"] >= 100)
    & (filtered["has_card"] == False)
]

st.write(
    f"""
    **{len(card_clients)} клиентов** совершают больше 100 операций
    в месяц, но пока не используют бизнес-карту.
    """
)


problem_clients = filtered[
    filtered["support_requests"] >= 4
]

problem_churn = problem_clients["churned"].mean() * 100

st.write(
    f"""
    У клиентов с четырьмя и более обращениями в поддержку
    отток составляет **{problem_churn:.1f}%**.
    """
)


with st.expander("Посмотреть данные"):
    st.dataframe(filtered)