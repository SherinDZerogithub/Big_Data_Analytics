import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# -------------------------------------------------
# 1. Load Your Dataset
# -------------------------------------------------
df = pd.read_csv("data/cleaned.csv")

df["Release_Date"] = pd.to_datetime(df["Release_Date"])
df["Viewing_Month"] = pd.to_datetime(df["Viewing_Month"])

df["Release_Year"] = df["Release_Date"].dt.year
df["Release_Month"] = df["Release_Date"].dt.month
df["Viewing_Year"] = df["Viewing_Month"].dt.year
df["Viewing_Month_Num"] = df["Viewing_Month"].dt.month

# -------------------------------------------------
# 2. Create Charts
# -------------------------------------------------

# Scatter Plot: Rating vs Views
fig_scatter = px.scatter(
    df,
    x="Viewer_Rate",
    y="Number_of_Views",
    color="Category",
    size="Number_of_Views",
    hover_name="Film_Name",
    title="Viewer Rating vs Number of Views"
)

# Bar Chart: Views per Movie
fig_bar = px.bar(
    df,
    x="Film_Name",
    y="Number_of_Views",
    color="Category",
    title="Views per Movie"
)

# Line Chart: Views over Release Year
fig_year = px.line(
    df.sort_values("Release_Year"),
    x="Release_Year",
    y="Number_of_Views",
    markers=True,
    title="Number of Views by Release Year"
)

# Category Distribution Pie Chart
fig_pie = px.pie(
    df,
    names="Category",
    values="Number_of_Views",
    title="Category Contribution to Total Views"
)

# -------------------------------------------------
# 3. Build Dashboard Layout
# -------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Movie Analytics Dashboard", style={"text-align": "center"}),

    html.Div([
        html.Div([
            html.H3("Viewer Rating vs Views"),
            dcc.Graph(figure=fig_scatter)
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            html.H3("Views by Category"),
            dcc.Graph(figure=fig_pie)
        ], style={"width": "48%", "display": "inline-block", "float": "right"}),
    ]),

    html.H2("Views per Movie"),
    dcc.Graph(figure=fig_bar),

    html.H2("Views by Release Year"),
    dcc.Graph(figure=fig_year)
])

# -------------------------------------------------
# 4. Run the App
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

