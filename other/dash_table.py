import QuantLib as ql
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.figure_factory as ff
import plotly.express.trendline_functions
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_test import dash_table, Dash, dcc, Output, Input, State, no_update, html

from findata.commons.constants.columns.base import SYMBOL_COL
from research.container import YieldCurvesContainer
from web.dash.factory.table import table_factory, table_container
from web.dash.utils import column_definitions

pd.options.mode.chained_assignment = None

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 dbc.icons.BOOTSTRAP])

val_date = ql.Date(30, 12, 2021)
ql.Settings.instance().evaluationDate = val_date

container = YieldCurvesContainer(val_date)
debt_secs_table = container.debt_secs_table
debt_secs = debt_secs_table.get_table()

col_defs = column_definitions(debt_secs)

table = table_factory('debt_secs', debt_secs)


# table = dash_table.DataTable(columns=col_defs,
#                              id='debt_secs-table',
#                              data=debt_secs.to_dict('records'),
#
#                              persistence=True,
#                              persistence_type='local',
#
#                              fixed_rows={'headers': True},
#                              fixed_columns={'headers': True, 'data': 1},
#                              # sort_mode="multi",
#                              # column_selectable='single',
#                              # row_selectable='single',
#                              # style_cell={'textAlign': ['left', 'center'], },  # 'padding': '5px',
#                              sort_action='native',
#                              filter_action='native',
#                              style_header={
#                                  # 'backgroundColor': 'gray',
#                                  'fontWeight': 'bold',
#                                  'textAlign': 'center',
#                                  'font-size': 12,
#                                  # 'width': '100px',
#                                  # 'maxWidth': '400px',
#                                  # 'minWidth': '200px',
#                              },
#                              style_data={
#                                  # 'width': '100px',
#                                  'maxWidth': '400px',
#                                  'minWidth': '100px',
#
#                              },
#                              style_table={
#                                  'height': 1500,  # default is 500
#                                  # 'minHeight': '100%',
#                                  'minWidth': '100%',
#                                  'font-size': 11,
#                                  # 'overflowX': '100%', # 'auto'
#
#                              },
#                              style_data_conditional=[
#                                  {
#                                      'if': {
#                                          'column_id': SYMBOL_COL,
#                                      },
#                                      'backgroundColor': 'yellow',
#                                      'fontWeight': 'bold',
#                                  },
#                                  {
#                                      'if': {
#                                          'column_type': 'text',
#
#                                      },
#                                      'textAlign': 'center',
#                                  },
#                                  {
#                                      'if': {
#                                          'column_type': 'datetime',
#
#                                      },
#                                      'textAlign': 'center',
#                                  },
#                              ],
#
#                              )

# drop_down = dcc.Dropdown(
#     id='debt_secs-table_dropdown',
#     options=[{'label': c, 'value': c} for c in debt_secs.columns],
#     multi=True,
#     clearable=True,
# )
def settings_factory(df):
    items = []
    for col in df.columns:
        row = html.Div([html.Label([col],
                                   style={
                                       'min-width': 120,
                                       "text-align": "center",
                                       'font-size': '0.9rem',
                                       'margin-left': 10, 'margin-right': 10,
                                       'margin-top': 'auto', 'margin-bottom': 'auto'
                                   }),
                        dcc.Checklist(options=[{"label": col, "value": col}],
                                      # id='debt_secs-table_dropdown',
                                      persistence=True,
                                      persistence_type='local',
                                      value=[col],
                                      style={'display': 'flex'},
                                      ),

                        ],
                       # todo
                       draggable='True',
                       style={
                           'display': 'flex',
                           'justify-content': 'start', 'align-items': 'center',
                           'margin-top': 5, 'margin-bottom': 5
                       })
        items.append(row)

    setting = dbc.DropdownMenu(label='Settings',
                               id='debt_secs-table_settings',
                               children=items,
                               # align_end=True,
                               color='secondary',
                               direction='down',
                               )

    return setting


setting = settings_factory(debt_secs)

table_container = table_container('debt_secs')
table_container.children = table

app.layout = dbc.Container(
    children=[setting, table_container],

    style={'width': '100%', 'height': '100vh'},
    fluid=True,

)


@app.callback(
    Output('debt_secs-table', 'columns'),
    Output('debt_secs-table', 'data'),
    Input('debt_secs-table_dropdown', 'value'),
    State('debt_secs-table_container', 'children'),
    State('debt_secs-table_settings', 'children'),
)
def display_table(value, table, settings):
    df = debt_secs[value]
    columns = column_definitions(df)
    data = df.to_dict("records")

    return columns, data


if __name__ == '__main__':
    app.run_server(debug=True)
