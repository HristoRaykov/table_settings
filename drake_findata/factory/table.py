import dash_bootstrap_components as dbc
from dash import dash_table, html

from web.dash.utils import column_definitions, generate_id
from findata.commons.constants.columns.base import SYMBOL_COL

COLUMNS_WIDTH = 120
VISIBLE_WIDTH = 100
COLOR_WIDTH = 100
SETTINGS_TABLE_WIDTH = COLUMNS_WIDTH + VISIBLE_WIDTH + COLOR_WIDTH

TABLE_HEIGHT = '77vh'


def settings_header_factory(prefix=None):
    visibility_id = generate_id(prefix, 'visibility')
    color_id = generate_id(prefix, 'color')

    settings_header = html.Thead([html.Tr([html.Th(children='Columns', colSpan=1, style={'width': COLUMNS_WIDTH,
                                                                                         'padding': 1}),
                                           html.Th(children=html.Div('Visible',
                                                                     style={'display': 'flex',
                                                                            'justify-content': 'center',
                                                                            }
                                                                     ),
                                                   colSpan=1,
                                                   style={'width': VISIBLE_WIDTH, 'padding': 1}),
                                           html.Th(children=html.Div('Color Scale',
                                                                     style={'display': 'flex',
                                                                            'justify-content': 'center',
                                                                            }
                                                                     ),
                                                   colSpan=1,
                                                   style={'width': COLOR_WIDTH, 'padding': 1})],

                                          ),
                                  html.Tr([html.Th(children='select all', colSpan=1, style={'width': COLUMNS_WIDTH,
                                                                                            'padding': 1}),
                                           html.Th(children=dbc.Checkbox(id=visibility_id,
                                                                         value=True,
                                                                         persistence=True,
                                                                         persistence_type='local',
                                                                         style={'display': 'flex',
                                                                                'justify-content': 'center',
                                                                                'align-items': 'center',
                                                                                # 'margin-right': 14,
                                                                                },
                                                                         ),
                                                   colSpan=1,
                                                   style={'width': VISIBLE_WIDTH, 'padding': 1},
                                                   ),
                                           html.Th(children=dbc.Checkbox(id=color_id,
                                                                         value=True,
                                                                         persistence=True,
                                                                         persistence_type='local',
                                                                         style={'display': 'flex',
                                                                                'justify-content': 'center',
                                                                                'align-items': 'center',
                                                                                # 'margin-right': 24,
                                                                                },
                                                                         ),
                                                   colSpan=1,
                                                   style={'width': COLOR_WIDTH, 'padding': 1},
                                                   )],
                                          )
                                  ],
                                 style={'display': 'block', },
                                 )
    ids = {
        'visibility_select_all': visibility_id,
        'color_select_all': color_id,
    }

    return ids, settings_header


def column_setting_factory(name, prefix=None):
    col_id = generate_id(prefix, name)
    col_visibility_id = generate_id(prefix, 'visibility', name)
    col_color_id = generate_id(prefix, 'color', name)
    row = html.Tr(
        # html.Div(
        [html.Td(name, style={'width': COLUMNS_WIDTH}, ),
         html.Td(dbc.Checkbox(id=col_visibility_id,
                              value=True,
                              persistence=True,
                              persistence_type='local',
                              style={'display': 'flex',
                                     'justify-content': 'center',
                                     'align-items': 'center'},
                              ),
                 style={'width': VISIBLE_WIDTH},
                 ),
         html.Td(dbc.Checkbox(id=col_color_id,
                              value=True,
                              persistence=True,
                              persistence_type='local',
                              style={'display': 'flex',
                                     'justify-content': 'center',
                                     'align-items': 'center'},
                              ),
                 style={'width': COLOR_WIDTH},
                 )
         ],

        style={'height': 35, 'overflow': 'hidden',
               'display': 'flex',
               'justify-content': 'center',
               'align-items': 'center',
               'padding': 0,
               },
        # ),
        id=col_id,
    )

    ids = {'col': name,
           'col_visibility': col_visibility_id,
           'col_color': col_color_id,
           }

    return ids, row


def settings_table_factory(columns, prefix=None):
    rows = []
    ids = {'cols': [], 'col_visibilities': [], 'col_colors': []}

    for col in columns:
        row_ids, row = column_setting_factory(col, prefix=prefix)
        ids['cols'].append(row_ids['col'])
        ids['col_visibilities'].append(row_ids['col_visibility'])
        ids['col_colors'].append(row_ids['col_color'])
        rows.append(row)

    drag_container_id = generate_id(prefix, 'drag_container')
    ids['drag_container'] = drag_container_id

    table_body = html.Tbody(rows,
                            id=drag_container_id,
                            style={
                                # 'overflow': 'auto',
                                'overflow-y': 'scroll',
                                'display': 'block',
                                'max-height': TABLE_HEIGHT,
                            }
                            )

    header_ids, settings_header = settings_header_factory(prefix)
    ids.update(header_ids)

    table = dbc.Table([settings_header, table_body],
                      bordered=False,
                      responsive=True,
                      hover=True,
                      striped=True,
                      style={'display': 'block', 'width': SETTINGS_TABLE_WIDTH},  # 'block', table

                      )

    # tbl_cont = html.Div(table, style={'display': 'block', 'height': 700, 'overflow-y': 'auto'}, id='settings_table', )

    return ids, table


def settings_container(columns, prefix=None):
    ids = dict()

    sett_ids, table = settings_table_factory(columns, prefix=None)
    ids.update(sett_ids)

    freeze_col_input = dbc.Container([dbc.Label(['Freeze Cols:'],
                                                style={
                                                    'text-align': 'center',
                                                    'font-size': '0.8rem',
                                                    'margin-right': 3,
                                                    # 'margin-top': 'auto', 'margin-bottom': 'auto'
                                                }),
                                      dbc.Input(type="number", size='sm', min=0, step=1,
                                                id='freeze-cols',
                                                persistence=True,
                                                persistence_type='local',
                                                style={'width': 50}), ],
                                     fluid=True,
                                     style={'display': 'flex',
                                            'justify-content': 'start',
                                            'align-items': 'center',
                                            'padding': 0, },
                                     )

    sort_mode_input = dbc.Container(html.Div([dbc.Label(['Sort Mode:'],
                                                        style={
                                                            'text-align': 'center',
                                                            'font-size': '0.8rem',
                                                            'margin-right': 3,
                                                            # 'margin-top': 'auto', 'margin-bottom': 'auto'
                                                        }),
                                              dbc.Select(options=[{'label': 'single', 'value': 'single'},
                                                                  {'label': 'multi', 'value': 'multi'}],
                                                         value='single',
                                                         id='sort-mode',
                                                         persistence=True,
                                                         persistence_type='local',
                                                         size='sm',
                                                         style={'width': 100}
                                                         ), ],
                                             style={'display': 'flex',
                                                    'justify-content': 'start',
                                                    'align-items': 'center',
                                                    'padding': 0, }),
                                    fluid=True,
                                    style={'display': 'flex',
                                           'justify-content': 'end',
                                           'align-items': 'center',
                                           'padding': 0, },
                                    )

    settings_apply_btn_id = generate_id(prefix, 'settings_apply_btn')
    ids['settings_apply_btn'] = settings_apply_btn_id

    dd_container = dbc.Container([table,
                                  dbc.Container([freeze_col_input, sort_mode_input],
                                                fluid=True,
                                                style={'display': 'flex',
                                                       'justify-content': 'start',
                                                       'align-items': 'center',
                                                       'padding': 0,
                                                       'margin-left': 0, 'margin-right': 0,
                                                       'margin-top': 10, 'margin-bottom': 10,
                                                       }
                                                ),
                                  html.Div(dbc.Button('Apply',
                                                      id=settings_apply_btn_id,
                                                      size='sm',
                                                      color='secondary',
                                                      outline=True,
                                                      ),
                                           style={'display': 'flex', 'justify-content': 'center'}
                                           )
                                  ],
                                 fluid=True,
                                 style={'display': 'block', 'justify-content': 'center', 'overflowY': 'auto'})
    settings_id = generate_id(prefix, 'settings')
    ids['settings'] = settings_id
    settings = dbc.DropdownMenu(label="Settings",
                                children=dd_container,
                                color='secondary',
                                size='sm',
                                id=settings_id,

                                )

    settings_container = dbc.Container(
        children=[settings],
        style={'display': 'flex',
               'justify-content': 'start',
               'align-items': 'center',
               'padding-bottom': 4,
               'padding-left': 0,
               'padding-right': 0,
               },
        fluid=True,
    )

    return ids, settings_container


def table_factory(df, prefix=None):
    ids = dict()

    col_defs = column_definitions(df)
    table_id = generate_id(prefix, 'table')
    ids['table'] = table_id

    table_cont_id = generate_id(prefix, 'table_container')
    ids['table_container'] = table_cont_id

    table = dash_table.DataTable(columns=list(col_defs.values()),
                                 # id=table_id,
                                 data=df.to_dict('records'),

                                 persistence=True,
                                 persistence_type='local',

                                 fixed_rows={'headers': True},
                                 fixed_columns={'headers': True, 'data': 1},
                                 # sort_mode="multi",
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
                                     'min-width': '100%',
                                     'max-width': '100%',
                                     'width': '100%',
                                     'font-size': 11,
                                     'overflowX': '100%',

                                 },
                                 style_data_conditional=[
                                     {
                                         'if': {
                                             'column_id': SYMBOL_COL,
                                         },
                                         'backgroundColor': 'yellow',
                                         'fontWeight': 'bold',
                                     },
                                     {
                                         'if': {
                                             'column_type': 'text',

                                         },
                                         'textAlign': 'center',
                                     },
                                     {
                                         'if': {
                                             'column_type': 'datetime',

                                         },
                                         'textAlign': 'center',
                                     },
                                 ],
                                 css=[
                                     {'selector': 'table', 'rule': 'width: 100%;'},
                                     {
                                         'selector': '.dash-spreadsheet.dash-freeze-top,.dash-spreadsheet.dash-virtualized',
                                         'rule': 'max-height: 80vh;'}],

                                 )

    table_panel = dbc.Container(
        id=table_cont_id,
        children=[html.Div(table, id=table_id)],
        style={
            'width': '100%',
            'margin-left': 'auto', 'margin-right': 'auto',
            'padding-top': 0, 'padding-bottom': 12,
            'padding-left': 0, 'padding-right': 0,
            'display': 'table',
        },
        fluid=True,
    )

    return ids, table_panel


def table_container(df, prefix=None):
    ids = dict()

    table_ids, table = table_factory(df, prefix)
    ids.update(table_ids)
    sett_ids, settings = settings_container(df.columns, prefix=None)
    ids.update(sett_ids)

    table_container = dbc.Container(
        children=[html.Div(children=settings,

                           ),
                  html.Div(children=table,
                           ),
                  ],
        style={
            'width': '100%',
            'margin-left': 'auto', 'marginRight': 'auto',
            'padding-top': 12, 'paddingBottom': 12,
            'display': 'table',
        },
        fluid=True,
    )
    return ids, table_container
