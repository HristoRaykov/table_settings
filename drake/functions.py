import dash_bootstrap_components as dbc
import numpy as np
from dash_test import dash_table, html
from dash_test.dash_table.Format import Align

from constants import *

SETTINGS_HEADER = html.Thead([html.Tr([html.Th(children='Columns', colSpan=1, style={'width': COLUMNS_WIDTH}),
                                       html.Th(children=html.Div('Visible',
                                                                 style={'display': 'flex', 'justify-content': 'center'}
                                                                 ),
                                               colSpan=1,
                                               style={'width': VISIBLE_WIDTH}),
                                       html.Th(children=html.Div('Color Scale',
                                                                 style={'display': 'flex', 'justify-content': 'center'}
                                                                 ),
                                               colSpan=1,
                                               style={'width': COLOR_WIDTH})],

                                      ),
                              html.Tr([html.Th(children='select all', colSpan=1, style={'width': COLUMNS_WIDTH}),
                                       html.Th(children=dbc.Checkbox(id='visibility',
                                                                     value=True,
                                                                     persistence=True,
                                                                     persistence_type='local',
                                                                     style={'display': 'flex',
                                                                            'justify-content': 'center',
                                                                            'align-items': 'center',
                                                                            'margin-right': 14,
                                                                            },
                                                                     ),
                                               colSpan=1,
                                               style={'width': VISIBLE_WIDTH},
                                               ),
                                       html.Th(children=dbc.Checkbox(id='color',
                                                                     value=True,
                                                                     persistence=True,
                                                                     persistence_type='local',
                                                                     style={'display': 'flex',
                                                                            'justify-content': 'center',
                                                                            'align-items': 'center',
                                                                            'margin-right': 24,
                                                                            },
                                                                     ),
                                               colSpan=1,
                                               style={'width': COLOR_WIDTH},
                                               )],
                                      )
                              ],
                             style={'display': 'block', },
                             )


def generate_id(*args):
    id = ID_SEP.join(args)

    return id


def find_element_by_id(children, id):
    for child in children:
        if isinstance(child, dict):
            props = child.get('props')
            if props is not None:
                el_id = props.get('id')
                if el_id == id:
                    return child

            chldren = props.get('children')
            if chldren:
                chld = find_element_by_id(chldren, id)
                if chld:
                    return chld

    return None


def column_definitions(df):
    col_defs = dict()
    for col in df.columns:
        t = df[col].dtype
        if t == np.float64:
            col_def = dict(id=col, name=col, type='numeric',
                           format=dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed).group(
                               True))
        elif t == np.int64:
            col_def = dict(id=col, name=col, type='numeric',
                           format=dash_table.Format.Format(align=Align.right).group(True))
        elif np.issubdtype(t, np.datetime64):
            col_def = dict(id=col, name=col, type='datetime',
                           format=dash_table.Format.Format(align=Align.center))
        else:
            col_def = dict(id=col, name=col, type='text',
                           format=dash_table.Format.Format(align=Align.left))

        col_defs[col] = col_def

    return col_defs


def column_setting_factory(name):
    row = html.Tr([html.Td(name, style={'width': COLUMNS_WIDTH}, ),
                   html.Td(dbc.Checkbox(id=generate_id('visibility', name),
                                        value=True,
                                        persistence=True,
                                        persistence_type='local',
                                        style={'display': 'flex',
                                               'justify-content': 'center',
                                               'align-items': 'center'},
                                        ),
                           style={'width': VISIBLE_WIDTH},
                           ),
                   html.Td(dbc.Checkbox(id=generate_id('color', name),
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
                  id=name,
                  )

    return row


def settings_table_factory(columns):
    rows = []
    for col in columns:
        row = column_setting_factory(col)
        rows.append(row)

    table_body = html.Tbody(rows,
                            id='drag_container',
                            style={
                                # 'overflow': 'auto',
                                'overflow-y': 'scroll',
                                'display': 'block',
                                'max-height': 700,
                            }
                            )

    table = dbc.Table([SETTINGS_HEADER, table_body],
                      bordered=False,
                      responsive=True,
                      hover=True,
                      striped=True,
                      style={'display': 'block', 'width': SETTINGS_TABLE_WIDTH},

                      )

    # tbl_cont = html.Div(table, style={'display': 'block', 'height': 700, 'overflow-y': 'auto'}, id='settings_table', )

    return table


def settings_container(columns):
    table = settings_table_factory(columns)

    dd_container = dbc.Container([table,
                                  html.Div(dbc.Button('Apply',
                                                      id='settings-apply-btn',
                                                      size='sm',
                                                      color='secondary',
                                                      outline=True,
                                                      ),
                                           style={'display': 'flex', 'justify-content': 'center'}
                                           )
                                  ],
                                 fluid=True,
                                 style={'display': 'block', 'justify-content': 'center', 'overflowY': 'auto'})

    settings = dbc.DropdownMenu(label="Settings",
                                children=dd_container,
                                color='secondary',

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

    return settings_container


def table_factory(df):
    col_defs = column_definitions(df)
    table = dash_table.DataTable(columns=list(col_defs.values()),
                                 data=df.to_dict('records'),
                                 fixed_rows={'headers': True},
                                 fixed_columns={'headers': True, 'data': 1},
                                 sort_mode='single',  # 'multi',
                                 persistence=True,
                                 persistence_type='local',
                                 # row_selectable='single',
                                 # column_selectable='multi',  # | 'multi' 'single'
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
                                 )

    return col_defs, table


def table_container(df):
    col_defs, table = table_factory(df)
    settings = settings_container(df.columns)

    table_panel = dbc.Container(
        id='table_container',
        children=[html.Div(id='settings',
                           children=settings,
                           ),
                  html.Div(id='table',
                           children=table,
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
    return col_defs, table_panel
