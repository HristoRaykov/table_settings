import dash_bootstrap_components as dbc
import numpy as np
from dash import dash_table, html, dcc
from dash.dash_table.Format import Align

from table_settings.settings.colors import styles_factory
from table_settings.settings.settings_dash import settings_factory
from table_settings.utils import generate_id

BASE_TABLE_FORMAT = [
    {'if': {'column_type': 'text', },
     'textAlign': 'center', },
    {'if': {'column_type': 'datetime', },
     'textAlign': 'center', },
]


def column_definitions(df):
    col_defs = dict()
    for col in df.columns:
        t = df[col].dtype
        if t == np.float64:
            col_def = dict(id=col, name=col, type='numeric',  # hideable=True,
                           format=dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed).group(
                               True))
        elif t == np.int64:
            col_def = dict(id=col, name=col, type='numeric',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.right).group(True))
        elif np.issubdtype(t, np.datetime64):
            col_def = dict(id=col, name=col, type='datetime',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.center))
        else:
            col_def = dict(id=col, name=col, type='text',  # hideable=True,
                           format=dash_table.Format.Format(align=Align.left))

        col_defs[col] = col_def

    return col_defs


def table_factory(df, width, height, prefix=None):
    ids = dict()

    col_defs = column_definitions(df)

    # table_cont_id = generate_id(prefix, 'table_container')
    # ids['table_container'] = table_cont_id

    table = dash_table.DataTable(columns=list(col_defs.values()),
                                 # id=table_id,
                                 data=df.to_dict('records'),
                                 fill_width=False,
                                 persistence=True,
                                 persistence_type='local',

                                 fixed_rows={'headers': True},
                                 fixed_columns={'headers': True, 'data': 0},
                                 sort_mode='single',
                                 # column_selectable='single',
                                 # row_selectable='single',
                                 # style_cell={'textAlign': ['left', 'center'], },  # 'padding': '5px',
                                 sort_action='native',
                                 filter_action='native',
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
                                     'width': width,
                                     'min-width': width,
                                     'max-width': width,
                                     'height': height,
                                     'min-height': height,
                                     'max-height': height,

                                     'font-size': 11,
                                     'overflowX': 'auto'

                                 },
                                 style_data_conditional=BASE_TABLE_FORMAT,
                                 # css=[
                                 #     # {'selector': 'table', 'rule': 'width: 97.5vw;'},
                                 #     {
                                 #         'selector': '.dash-spreadsheet.dash-freeze-top,.dash-spreadsheet.dash-virtualized',
                                 #         'rule': 'max-height: 80vh;'}],
                                 css=[{"selector": ".show-hide", "rule": "display: none"}]
                                 )

    return ids, col_defs, table


def table_panel_factory(df, width, height, prefix=None):
    ids = dict()
    table_cont_id = generate_id(prefix, 'table_container')
    ids['table_container'] = table_cont_id

    table_ids, col_defs, table = table_factory(df, width, height, prefix)
    ids.update(table_ids)
    table_id = generate_id(prefix, 'table')
    ids['table'] = table_id

    sett_ids, settings = settings_factory(df.columns, prefix=None)
    ids.update(sett_ids)
    settings_store_id = generate_id(prefix, 'settings_store')
    ids['settings_store'] = settings_store_id

    settings_panel = dbc.Container(
        children=[settings,
                  dcc.Store(id=settings_store_id, storage_type='local'),
                  # html.Div(dbc.Button(id=settings_close_btn_id, n_clicks=0), hidden=True)
                  ],
        style={'display': 'flex',
               'justify-content': 'start',
               'align-items': 'center',
               'padding-bottom': 4,
               'padding-left': 0,
               'padding-right': 0,
               },
        fluid=True,
    )

    table_panel = dbc.Container(
        children=[html.Div(table, id=table_id, )],
        style={
            'width': '100%',
            'margin-left': 'auto', 'margin-right': 'auto',
            'padding-top': 0, 'padding-bottom': 12,
            'padding-left': 0, 'padding-right': 0,
            'display': 'table',
        },
        fluid=True,
    )

    table_container = dbc.Container(
        children=[html.Div(children=settings_panel, ),
                  html.Div(children=table_panel, ),
                  ],
        style={
            'width': '100%',
            'margin-left': 'auto', 'marginRight': 'auto',
            'padding-top': 12, 'paddingBottom': 12,
            'display': 'table',
        },
        fluid=True,
        id=table_cont_id,
    )

    column_styles = styles_factory(df)

    return ids, col_defs, column_styles, table, settings, table_container
