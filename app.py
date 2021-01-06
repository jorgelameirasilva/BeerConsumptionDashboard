import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#ISO code 
iso_url = "https://www.iban.com/country-codes"
iso_df = pd.read_html(iso_url)[0]
iso_df = iso_df[["Country", "Alpha-3 code"]]
iso_df["Country"] = iso_df["Country"].str.lower()


#Beer and Wine data
url = "https://datahub.io/five-thirty-eight/alcohol-consumption/r/0.csv"
df = pd.read_csv(url)

df = df.merge(iso_df, left_on="country", right_on="Country")

df.drop(["Country"], axis=1, inplace=True)


def make_map(column="beer_servings"):
    fig = px.choropleth(df, locations="Alpha-3 code", color=column, hover_name= "country")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig



app = dash.Dash()


app.layout = html.Div([
    html.H1("Welcome to the dashboard !"),
    dcc.RadioItems(id="radio-items", 
            options=[
                {"label":"Beer Consumption", "value":"beer_servings"},
                {"label":"Wine Consumption", "value":"wine_servings"},
            ],
            value="beer_servings"),
    dcc.Graph(id="graph", figure=make_map())
])

@app.callback(
    [Output("graph", "figure")],
    [Input("radio-items", "value")]
)
def render_graph(v):
    return [make_map(v)]

app.run_server(debug=True)