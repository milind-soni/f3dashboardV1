"""
This app creates an animated sidebar using the dbc.Nav component and some local
CSS. Each menu item has an icon, when the sidebar is collapsed the labels
disappear and only the icons remain. Visit www.fontawesome.com to find
alternative icons to suit your needs!

dcc.Location is used to track the current location, a callback uses the current
location to render the appropriate page content. The active prop of each
NavLink is set automatically according to the current pathname. To use this
feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd 
import numpy as np 
import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.dash_table.Format import Group
import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go


PLOTLY_LOGO = "assets/f3logo.png"


mapbox_access_token = 'pk.eyJ1IjoibWlsaW5kc29uaSIsImEiOiJjbDRjc2ZxaTgwMW5hM3Bqbmlka3VweWVkIn0.AM0QzfbGzUZc04vZ6o2uaw'


df = pd.read_csv("profiling2.csv")
blackbold={'color':'black', 'font-weight': 'bold'}

sku_list = ["Apple", "Banana", "Mango"]
quality_list = ["A","B","C"]


app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
server = app.server

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("Dashboard"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-map-marker" ), html.Span("  Vendors")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span(" Analytics"),
                    ],
                    href="/calendar",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-users"),
                        html.Span("      Sales Team"),
                    ],
                    href="/messages",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

# content = html.Div(id="page-content", className="content")


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="end",
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Vendors", className="display-3", style={"color":"black","font-weight":"bold"})),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    className="shadow-sm p-3 mb-5 bg-white rounded",
    color="white",
    dark=True,
)


app.layout = html.Div([
    
    
    html.Div([dcc.Location(id="url"),navbar, sidebar]),

   html.Div([
            # Map-legend

            # html.Ul([
            #     html.Div(
            #         html.Img(src = app.get_asset_url('fff.webp')))
               
            # ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            # ),
dbc.Row(
dbc.Card(
    
        dbc.CardBody(
    
    [

            dbc.Row([
            # Borough_checklist
           

           dbc.Col(
            html.Div([
            html.Label(children=['SKU: '], style=blackbold),
            dcc.Dropdown(id='boro_name',
                    options=[{'label':str(b),'value':b} for b in sku_list],
                    value=[b for b in sku_list],multi=True
            ),]),
            width={"size": 4, "offset": 1},
            ),
            
            dbc.Col(
            html.Div([


            html.Label(children=['Quality Index: '], style=blackbold),
            dcc.Dropdown(id='quality',
                    options=[{'label':str(b),'value':b} for b in sorted(df['quality'].unique())],
                    value=[b for b in sorted(df['quality'].unique())],multi=True
            ),]
            ),
                        width={"size": 3, "offset": 0},

            ),

            # # Recycling_type_checklist
            # html.Label(children=['Quality Index '], style=blackbold),
            # dcc.Checklist(id='recycling_type',
            #         options=[{'label':str(b),'value':b} for b in quality_list],
            #         value=[b for b in quality_list],
            # ),
            dbc.Col(
            html.Div([
            html.Label(children=['Sales Exec Name: '], style=blackbold),
            dcc.Dropdown(id='sales_exec',
                    options=[{'label':str(b),'value':b} for b in sorted(df['Sales Exec Name'].unique())],
                    value=[b for b in sorted(df['Sales Exec Name'].unique())],multi=True),
            ]),
                        width={"size": 3, "offset": 0},

            ),
            ]
            
            )

            

   ],
        ),
   )
),

dbc.Row([

            html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'padding-top':'0px','padding-bottom':'10px','padding-left':'10px','height':'100vh'}
            )
        ]
        ),

])


        ],     

        ),






])

# set the content according to the current pathname
@app.callback(Output('graph', 'figure'),
              [Input('quality', 'value'),
              Input('sales_exec','value')])




def update_figure(chosen_quality,chosen_exec):
    df_sub = df[(df['quality'].isin(chosen_quality)) &
            (df['Sales Exec Name'].isin(chosen_exec))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['Longitude'],
                    lat = df_sub['Latitude'],
                    mode='markers',
                    marker={'color' :df_sub['Color']  , 'size' : 2*df['Total'] },
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':100}},
                    hoverinfo='text',
                    hovertext=df_sub['hov_text']
    )]


    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='streets',
                center=dict(
                     
                    lat=28.636534588228688,
                    lon=77.26948797090003
                ),
                pitch=40,
                zoom=11.5
            ),
        )
    }

def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the home page!")
    elif pathname == "/calendar":
        return html.P("This is your calendar... not much in the diary...")
    elif pathname == "/messages":
        return html.P("Here are all your messages")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)


