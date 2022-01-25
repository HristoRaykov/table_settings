import copy

import QuantLib as ql
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, Input, Output, State, callback_context, html, dcc, dash_table
from dash.dash_table.Format import Align

from table_settings.constants import TABLE_WIDTH, TABLE_EXPAND_HEIGHT, TABLE_SHRINK_HEIGHT, ID_SEP, \
    SETTINGS_TABLE_HEIGHT
from table_settings.settings.settings_dash import settings_table_factory
from table_settings.table import table_panel_factory, BASE_TABLE_FORMAT, column_definitions
from table_settings.utils import generate_test_table, find_element_by_id, generate_id

pd.options.mode.chained_assignment = None

COLUMN = 'Column'
POSITION = 'Position'
VISIBILITY = 'Visibility'

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 dbc.icons.BOOTSTRAP],

           )  # external_stylesheets=[dbc.themes.LITERA],

df = generate_test_table()

# todo build column settings dataframe
setts = pd.DataFrame({'Column': df.columns})
setts['Position'] = setts.index.astype(int)
setts['Visibility'] = 'true'

select_all = pd.DataFrame({COLUMN: ['select all'], POSITION: [None], VISIBILITY: ['true']})
#
setts = pd.concat([pd.DataFrame(select_all), setts], ignore_index=True)
# col_defs = column_definitions(setts)


# col_defs = [
#     dict(id=COLUMN, name=[COLUMN, 'select_all'], type='text', editable=False,
#          format=dash_table.Format.Format(align=Align.left)),
#     dict(id=POSITION, name=[POSITION, ''], type='numeric', editable=True,
#          format=dash_table.Format.Format(align=Align.right).group(True)),
#     dict(id=VISIBILITY, name=[VISIBILITY, ''], type='numeric', editable=True,
#          format=dash_table.Format.Format(align=Align.right).group(True)),
# ]

col_defs = [
    dict(id=COLUMN, name=COLUMN, type='text', editable=False,
         format=dash_table.Format.Format(align=Align.left)),
    dict(id=POSITION, name=POSITION, type='numeric', editable=True,
         format=dash_table.Format.Format(align=Align.right).group(True)),
    dict(id=VISIBILITY, name=VISIBILITY, type='text', presentation='dropdown', # editable=True,
         # format=dash_table.Format.Format(align=Align.right).group(True)
         ),
]

table = dash_table.DataTable(columns=col_defs,
                             # id=table_id,
                             data=setts.to_dict('records'),
                             editable=True,
                             fill_width=False,
                             persistence=True,
                             persistence_type='local',
                             merge_duplicate_headers=True,
                             fixed_rows={'headers': True, 'data': 1},
                             fixed_columns={'headers': True, 'data': 0},
                             # style_as_list_view=True,
                             # sort_mode='single',
                             # column_selectable='single',
                             # row_selectable='multi',
                             # style_cell={'textAlign': ['left', 'center'], },  # 'padding': '5px',
                             # sort_action='native',
                             # filter_action='native',
                             style_header={
                                 # 'backgroundColor': 'gray',
                                 'fontWeight': 'bold',
                                 'textAlign': 'center',
                                 'font-size': 12,

                             },
                             style_data={
                                 'max-width': '400px',
                                 'min-width': '100px',

                             },
                             style_table={
                                 # 'width': width,
                                 # 'min-width': width,
                                 # 'max-width': width,
                                 'height': SETTINGS_TABLE_HEIGHT,
                                 'min-height': SETTINGS_TABLE_HEIGHT,
                                 'max-height': SETTINGS_TABLE_HEIGHT,

                                 'font-size': 11,
                                 'overflowX': 'auto'

                             },
                             style_data_conditional=BASE_TABLE_FORMAT,
                             # css=[
                             #     # {'selector': 'table', 'rule': 'width: 97.5vw;'},
                             #     {
                             #         'selector': '.dash-spreadsheet.dash-freeze-top,.dash-spreadsheet.dash-virtualized',
                             #         'rule': 'max-height: 80vh;'}],
                             css=[{"selector": ".show-hide", "rule": "display: none"},
                                  {"selector": ".Select-menu-outer", "rule": 'display : block !important'}
                                  ],

                             dropdown={
                                 VISIBILITY: {
                                     'options': [{'label': 'True', 'value': 'true'},
                                                 {'label': 'False', 'value': 'false'}]
                                 },

                             },
                             # dropdown_conditional=[{
                             #     'if': {
                             #         'column_id': 'Neighborhood',  # skip-id-check
                             #         'filter_query': '{City} eq "NYC"'
                             #     },
                             #     'options': [
                             #         {'label': i, 'value': i}
                             #         for i in [
                             #             'Brooklyn',
                             #             'Queens',
                             #             'Staten Island'
                             #         ]
                             #     ]
                             # }]
                             )

app.layout = dbc.Container(children=[table],
                           id='debt_secs_layout',
                           style={'width': '100%',
                                  # 'max-width': '100%',
                                  'height': '96vh',
                                  },
                           fluid=True,

                           )

if __name__ == '__main__':
    app.run_server(debug=True)
