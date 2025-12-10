import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


# -------------------------------------------------
# 1. Load Your Dataset
# -------------------------------------------------
df = pd.read_csv("data/cleaned.csv")
monthly_views = pd.read_csv("data/Feature_Monthly_Views.csv")
total_views = pd.read_csv("data/Feature_Total_Views.csv")
processed_data = pd.read_csv("data/Processed_Film_Dataset.csv")

# Convert dates
df["Release_Date"] = pd.to_datetime(df["Release_Date"])
df["Viewing_Month"] = pd.to_datetime(df["Viewing_Month"])

df["Release_Year"] = df["Release_Date"].dt.year
df["Release_Month"] = df["Release_Date"].dt.month
df["Viewing_Year"] = df["Viewing_Month"].dt.year
df["Viewing_Month_Num"] = df["Viewing_Month"].dt.month

# ===========================================
# MERGING
# ===========================================
monthly_views["view_date"] = pd.to_datetime(
    monthly_views["view_year"].astype(str) + "-" +
    monthly_views["view_month"].astype(str) + "-01"
)

complete_data = monthly_views.merge(total_views, on="Film_Name", how="left")

film_features = processed_data[[
    "Film_Name", "Category", "Language", "Viewer_Rate",
    "Avg_Rating_Category", "Avg_Rating_Language"
]].drop_duplicates()

complete_data = complete_data.merge(film_features, on="Film_Name", how="left")

print("\nMerged dataset shape:", complete_data.shape)

# -------------------------------------------------
# 2. Plotly Charts (Dash Compatible)
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
    title="Views per Movie",
    color_continuous_scale="Viridis"
)

#Bar chart : top 10 movies.........
top_movies = total_views.sort_values(
    'Total_Views', ascending=False
).head(10)

top_bar = px.bar(
    top_movies,
    x="Total_Views",
    y="Film_Name",
    orientation="h",
    title="Top 10 Movies by Total Views",
    color="Total_Views",
    color_continuous_scale="Viridis"
)

# Invert y-axis so highest is on top
top_bar.update_layout(yaxis=dict(autorange="reversed"))

# Add value labels
top_bar.update_traces(
    text=top_movies["Total_Views"],
    textposition="outside",
    # optional, to show values
    width=0.8 
)


#total Views............
# Histogram of Total Views (Plotly)
fig_hist = px.histogram(
    total_views,
    x="Total_Views",
    nbins=30,
    marginal="rug",
    title="Distribution of Total Views"
)

# Add outline
fig_hist.update_traces(
    marker=dict(
        line=dict(
            width=1.5,
            color="black"
        )
    )
)

# Box Plot of Total Views (Plotly)
fig_box = px.box(
    total_views,
    y="Total_Views",
    title="Box Plot of Total Views"
)



# Line Chart: Monthly Views Trend
monthly_trend = (
    monthly_views.groupby(["view_year", "view_month"])["Monthly_Views"]
    .sum()
    .reset_index()
)

monthly_trend["date"] = pd.to_datetime(
    monthly_trend["view_year"].astype(str) + "-" +
    monthly_trend["view_month"].astype(str) + "-01"
)

fig_monthly = px.line(
    monthly_trend,
    x="date",
    y="Monthly_Views",
    markers=True,
    title="Monthly Views Trend (All Movies)"
)

# Line Chart: Views by Release Year
fig_year = px.line(
    df.sort_values("Release_Year"),
    x="Release_Year",
    y="Number_of_Views",
    markers=True,
    title="Number of Views by Release Year"
)


#category & language analysis Top 10 Categories by total Views...............
# Sort categories by total views
# ---- CATEGORY STATS ----
# Group by Category and calculate Total Views per Category
# Category Distribution Pie Chart
fig_pie = px.pie(
    df,
    names="Category",
    values="Number_of_Views",
    title="Category Contribution to Total Views"
)

#Total views by language
# ---------------------------------------
category_stats = (
    df.groupby('Category')['Number_of_Views']
      .sum()
      .reset_index()
      .sort_values('Number_of_Views', ascending=False)
)

category_bar = px.bar(
    category_stats,
    x="Category",              # Category on X-axis
    y="Number_of_Views",       # Views on Y-axis
    title="Total Views by Category",
    color="Number_of_Views",
    color_continuous_scale="Plasma"
)
# Improve layout
category_bar.update_layout(
    xaxis_tickangle=45, 
    height=600,
)
# Add value labels on top of bars
category_bar.update_traces(
    text=category_stats["Number_of_Views"],
    textposition="outside"
)


# Sort language category by total views
# ---- CATEGORY STATS ----
# Group by Language Category and calculate Total Views per Category
# Category Distribution Pie Chart
figL_pie = px.pie(
    df,
    names="Language",
    values="Number_of_Views",
    title="Language Contribution to Total Views"
)

#Total views by language
# ---------------------------------------
categoryl_stats = (
    df.groupby('Language')['Number_of_Views']
      .sum()
      .reset_index()
      .sort_values('Number_of_Views', ascending=False)
)

categoryl_bar = px.bar(
    categoryl_stats,
    x="Language",              # Category on X-axis
    y="Number_of_Views",       # Views on Y-axis
    title="Total Views by Category",
    color="Number_of_Views",
    color_continuous_scale="Speed"
)
# Improve layout
categoryl_bar.update_layout(
    xaxis_tickangle=45,
    height=600,
)
# Add value labels on top of bars
categoryl_bar.update_traces(
    text=category_stats["Number_of_Views"],
    textposition="outside"
)


#Analysis with average values_______--------
#---------------------------------------------------
correlation_cols = [
    'Viewer_Rate', 
    'Number_of_Views',
    'Avg_Rating_Category', 
    'Avg_Rating_Language'
]

# Keep only existing columns
available_cols = [col for col in correlation_cols if col in processed_data.columns]

correlation_data = processed_data[available_cols]

corr_matrix = correlation_data.corr()


fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu',
    title="Correlation Matrix",
    aspect="auto"
)

fig_corr.update_layout(
    title_font=dict(size=18, family="Arial", color="black"),
    width=700,
    height=600
)

# --------------------------------------------------
# Release Month vs Performance (Plotly version)
# --------------------------------------------------

processed_data['Release_Month'] = pd.to_datetime(processed_data['Release_Date']).dt.month

month_performance = processed_data.groupby('Release_Month').agg({
    'Number_of_Views': ['mean', 'sum', 'count'],
    'Viewer_Rate': 'mean'
}).round(2)

# Flatten multi-index
month_performance.columns = ['_'.join(col).strip() for col in month_performance.columns]
month_performance.reset_index(inplace=True)


# Average Views (Line + Fill)
# -----------------------------

figm_avg_views = go.Figure()

figm_avg_views.add_trace(go.Scatter(
    x=month_performance['Release_Month'],
    y=month_performance['Number_of_Views_mean'],
    mode="lines+markers",
    fill="tozeroy"
))

figm_avg_views.update_layout(
    title="Average Views by Release Month",
    xaxis_title="Month",
    yaxis_title="Average Views",
    width=700,
    height=450
)

#Total Views by Month (Bar)
# -----------------------------

figm_total_views = px.bar(
    month_performance,
    x="Release_Month",
    y="Number_of_Views_sum",
    color="Release_Month",
    color_continuous_scale="Viridis",
    title="Total Views by Release Month"
)

figm_total_views.update_layout(
    width=700,
    height=450,
    xaxis_title="Month",
    yaxis_title="Total Views"
)

# Movie Count (Pie Chart)
# -----------------------------

figm_pie = px.pie(
    month_performance,
    values="Number_of_Views_count",
    names="Release_Month",
    title="Movie Releases by Month"
)

figm_pie.update_traces(textinfo="percent")
figm_pie.update_layout(width=700, height=450)



#Rating vs Month (Bubble Chart)
# -----------------------------

fig_rating = px.scatter(
    month_performance,
    x="Release_Month",
    y="Viewer_Rate_mean",
    size="Number_of_Views_sum",
    opacity=0.7,
    title="Rating by Release Month (bubble size = total views)"
)

# Bubble Chart
fig_rating.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Rating",
    height=450,  # Match heatmap height
    width=600,   # Match heatmap width
    margin=dict(l=60, r=20, t=80, b=50)  # Similar margins
)


december_movies = monthly_views[
    (monthly_views['view_year'] == 2025) & (monthly_views['view_month'] == 12)
].sort_values('Monthly_Views', ascending=False).head(10)

fig_dec_top10 = px.bar(
    december_movies,
    x="Monthly_Views",
    y="Film_Name",
    orientation="h",
    title="Top 10 Movies in December 2025",
    color="Monthly_Views",
    color_continuous_scale="Viridis"
)
fig_dec_top10.update_layout(yaxis=dict(autorange="reversed"))
# -------------------------------------------------
# NEW: Heatmap of Views by Month and Day of Week
# -------------------------------------------------

# Create day of week from viewing month
df['Day_of_Week'] = df['Viewing_Month'].dt.dayofweek
df['Month_Name'] = df['Viewing_Month'].dt.month_name()
df['Day_Name'] = df['Viewing_Month'].dt.day_name()

# Create a pivot table for heatmap
heatmap_data = df.groupby(['Month_Name', 'Day_Name'])['Number_of_Views'].sum().reset_index()

# Order months chronologically
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Order days of week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create pivot for heatmap
pivot_heatmap = heatmap_data.pivot(index='Month_Name', columns='Day_Name', values='Number_of_Views')

# Reindex to ensure correct order
pivot_heatmap = pivot_heatmap.reindex(index=month_order, columns=day_order)

# Fill NaN values with 0
pivot_heatmap = pivot_heatmap.fillna(0)

# Create heatmap with better sizing
fig_heatmap = go.Figure(data=go.Heatmap(
    z=pivot_heatmap.values,
    x=pivot_heatmap.columns,
    y=pivot_heatmap.index,
    colorscale='Viridis',
    colorbar=dict(
        title="Total Views",
        title_font=dict(size=12),
        thickness=15,
        len=0.8
    ),
    hoverongaps=False,
    text=pivot_heatmap.values,
    texttemplate="%{text:,.0f}",
    textfont={"size": 10, "color": "white"},
    hovertemplate='<b>%{y} - %{x}</b><br>' +
                  'Total Views: %{z:,.0f}<extra></extra>'
))

# Update layout with better margins and sizing
# Update layout with better margins and sizing
fig_heatmap.update_layout(
    title={
        'text': "Heatmap: Viewing Patterns by Month and Day of Week",
        'font': {'size': 18},  # Smaller title
        'y': 0.92,  # Adjusted position
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis=dict(
        title="Day of Week",
        title_font=dict(size=12),  # Smaller font
        tickfont=dict(size=10)  # Smaller ticks
    ),
    yaxis=dict(
        title="Month",
        title_font=dict(size=12),  # Smaller font
        tickfont=dict(size=10)  # Smaller ticks
    ),
    height=450,  # Reduced from 600 to 450
    width=600,   # Reduced from 800 to 600 for better fit
    margin=dict(l=60, r=20, t=80, b=50),  # Adjusted margins
    plot_bgcolor='white'
)
# Add grid lines for better readability
fig_heatmap.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig_heatmap.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# -------------------------------------------------
# Build Dashboard Layout
# -------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Movie Analytics Dashboard", style={"text-align": "center", "font-size":"60px"}),

    html.Div([
        html.Div([
            html.H3("Viewer Rating vs Views", style={"text-align": "center"}),
            dcc.Graph(figure=fig_scatter)
        ], style={"width": "48%", "display": "inline-block","border": "2px solid black","margin": "10px"}),

        html.Div([
            html.H3("Top 10 Movies by Total Views", style={"text-align": "center"}),
            dcc.Graph(figure=top_bar),
        ], style={"width": "48%", "display": "inline-block","border": "2px solid black","margin": "10px"})

        
    ],style={
            "border": "2px solid black",  # black outline
            "padding": "10px",             # optional: add some padding inside
            "margin": "10px"  
            } 
    ),

    # html.Div([
    #     html.H2("Distribution of Total Views", style={"text-align": "center","font-size":"40px"}),
    #     html.Div([
    #         html.H3("Distribution of Total Views", style={"text-align": "center","font-size":"25px"}),
    #         dcc.Graph(figure=fig_hist),
    #     ], style={"width": "48%", "display": "inline-block","border": "2px solid black","margin": "10px"}),

    #     html.Div([
    #         html.H3("Box Plot of Total Views", style={"text-align": "center","font-size":"25px"}),
    #         dcc.Graph(figure=fig_box),
    #     ], style={"width": "48%", "display": "inline-block", "float": "right","border": "2px solid black","margin": "10px"}),
    #                 # optional: spacing around the div
    # ],style={
    #         "border": "2px solid black",  # black outline
    #         "padding": "10px",
    #         "margin": "10px"  
    #         } 
    # ),

    html.Div([
        html.H2("Categary And Language Analysis", style={"text-align": "center","font-size":"40px"}),
        html.Div([
            html.H3("Top 10 Categories by Total Views", style={"text-align": "center","font-size":"25px"}),
            dcc.Graph(figure=category_bar),
        ], style={"width": "48%", "display": "inline-block","border": "2px solid black","margin": "1px"}),

    #     html.Div([
    #         html.H3("Views by Category", style={"text-align": "center","font-size":"25px"}),
    #         dcc.Graph(figure=fig_pie),
    #     ], style={"width": "50%", "display": "inline-block", "float": "right","border": "2px solid black","margin": "1px"}),
    # ]
       html.Div([
            html.H3("Views by Language", style={"text-align": "center","font-size":"25px"}),
            dcc.Graph(figure=figL_pie),
        ], style={"width": "50%", "display": "inline-block", "float": "right","border": "2px solid black","margin": "1px"}),
    ],style={
            "border": "2px solid black",  # black outline
            "padding": "10px",             # optional: add some padding inside
            "margin": "10px"  
            } 
    ),


html.Div([
    html.H2("Seasonal Viewing Patterns",
            style={"text-align": "center", "font-size": "40px"}),

    html.Div([
        # Bubble Chart (Left)
        html.Div([
            html.H3("Rating vs Month (Bubble Chart)",
                    style={"text-align": "center", "font-size": "25px"}),

            dcc.Graph(figure=fig_rating,
                      style={"height": "450px"}),
        ], style={
            "flex": "1",
            "border": "2px solid black",
            "padding": "10px",
            "margin": "5px",
            "box-shadow": "2px 2px 10px #888888",
            "border-radius": "10px",
            "height": "550px"
        }),

        # Heatmap (Right)
        html.Div([
            html.H3("Monthly Viewing Heatmap",
                    style={"text-align": "center", "font-size": "25px"}),

            dcc.Graph(figure=fig_heatmap,
                      style={"height": "450px"}),
        ], style={
            "flex": "1",
            "border": "2px solid black",
            "padding": "10px",
            "margin": "5px",
            "box-shadow": "2px 2px 10px #888888",
            "border-radius": "10px",
            "height": "550px"
        }),

    ], style={
        "width": "100%",
        "display": "flex",
        "justify-content": "center",
        "align-items": "stretch"
    })
]),

    html.H2("Views by Release Year", style={"text-align": "center","font-size":"40px"}),
    dcc.Graph(figure=fig_year),

    html.H2("Monthly Views Trend", style={"text-align": "center","font-size":"40px"}),
    dcc.Graph(figure=fig_monthly)
])

# -------------------------------------------------
# 4. Run the App
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
