import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import datetime
from dash.dependencies import Output, Input

#Tablesheets to be read are from excel file. So they are stored to different dataframes
#Read data into pandas dataframe
df_products = pd.read_excel(
    r'C:\Users\cnwokocha.SOFTALLIANCE\Desktop\py4e\project_test\products.xlsx',
    sheet_name='product',)
df_payments = pd.read_excel(
    r'C:\Users\cnwokocha.SOFTALLIANCE\Desktop\py4e\project_test\products.xlsx',
    sheet_name='Payments',)
df_issues = pd.read_excel(
    r'C:\Users\cnwokocha.SOFTALLIANCE\Desktop\py4e\project_test\products.xlsx',
    sheet_name='issues',)
df_p_owners = pd.read_excel(
    r'C:\Users\cnwokocha.SOFTALLIANCE\Desktop\py4e\project_test\products.xlsx',
    sheet_name='product owners',)

df_payments['Date'] = pd.to_datetime(df_payments['Payment Date'], errors='coerce', unit='s')
df_payments.head()


# data = pd.read_csv(r'C:\Users\cnwokocha.SOFTALLIANCE\Desktop\py4e\project_test\avocado.csv')
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)

#============================Style CSS================================================
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # Run app using WSGI server (Heroku)
app.title = "Soft Alliance: Data Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=app.get_asset_url('SAAR.png'), className="header-emoji"),
                html.H1(
                    children="BILLING & PAYMENTS DEPARTMENT", className="header-title"
                ),
                html.P(
                    children="Analysis of Products",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="ProductName", className="menu-title"),
                        dcc.Dropdown(
                            id="ProductName-filter",
                            options=[
                                {"label": ProductName, "value": ProductName}
                                for ProductName in np.sort(df_products.ProductName.unique())
                            ],
                            value="SoftSuite",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="p_owner", className="menu-title"),
                        dcc.Dropdown(
                            id="p_owner-filter",
                            options=[
                                {"label": p_owner, "value": p_owner}
                                for p_owner in np.sort(df_p_owners.Surname.unique())
                            ],
                            value="Okobi",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=df_payments.Date.min().date(),
                            max_date_allowed=df_payments.Date.max().date(),
                            start_date=df_payments.Date.min().date(),
                            end_date=df_payments.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("ProductName-filter", "value"),
        Input("p_owner-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(ProductName, p_owner, start_date, end_date):
    mask = (
        (df_products.ProductName == ProductName)
        & (df_p_owners.Surname == p_owner)
        & (df_payments.Date >= start_date)
        & (df_payments.Date <= end_date)
    )
    filtered_df_po = df_p_owners.loc[mask, :]
    filtered_df_payments = df_payments.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_df_payments["Date"],
                "y": filtered_df_po["ProductOwnerID"],
                "type": "bar",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_df_payments["Date"],
                "y": filtered_df_po["ProductOwnerID"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
    