import plotly.graph_objects as go
import plotly.express as px

def price_trend_chart(price_history: list, title: str):
    if not price_history:
        return go.Figure()
    dates = [r["scraped_at"] for r in price_history]
    prices = [r["price"] for r in price_history]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=prices,
        mode="lines+markers",
        name="Price",
        line=dict(color="#667eea", width=2),
        marker=dict(size=4)
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="sans-serif"),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    return fig

def price_distribution_chart(products: list):
    if not products:
        return go.Figure()
    prices = [p["current_price"] for p in products]
    fig = px.histogram(
        x=prices, nbins=30,
        title="Price Distribution",
        labels={"x": "Price", "y": "Count"},
        color_discrete_sequence=["#667eea"]
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig

def category_bar_chart(products: list):
    if not products:
        return go.Figure()
    from collections import Counter
    cats = Counter(p["category"] for p in products)
    fig = px.bar(
        x=list(cats.keys()),
        y=list(cats.values()),
        title="Products by Category",
        labels={"x": "Category", "y": "Count"},
        color_discrete_sequence=["#764ba2"]
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig

def rating_chart(products: list):
    if not products:
        return go.Figure()
    ratings = [p["rating"] for p in products if p.get("rating")]
    fig = px.histogram(
        x=ratings, nbins=10,
        title="Rating Distribution",
        labels={"x": "Rating", "y": "Count"},
        color_discrete_sequence=["#f6d365"]
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig