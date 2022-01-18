import dash_bootstrap_components as dbc
import numpy as np
from dash import dash_table, html
from dash.dash_table.Format import Align
from dash_draggable import GridLayout

from other.table_settings.constants import *
from other.table_settings.constants import label_style


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


def settings_container(columns):
    cls_btn = dbc.Button(class_name="btn-close",
                         id='settings-modal-close-btn',
                         style={'display': 'flex', 'justify-content': 'end', })

    cols = [dbc.Col([dbc.Label(col, style={'display': 'flex', 'align-items': 'end', })],
                    style={'display': 'flex',
                           'align-items': 'end',
                           'font-weight': '600',
                           'justify-content': 'center', }) for col in SETTINGS_COLS]
    header = dbc.Container([dbc.Row(cols,
                                    style=flex_center,
                                    ),
                            html.Hr(style={'display': 'flex',
                                           'margin-top': 0,
                                           'margin-bottom': 0,
                                           'align-items': 'center',
                                           'justify-content': 'center',
                                           'padding': 0,
                                           }
                                    ),
                            dbc.Row([dbc.Col([dbc.Label('select all',
                                                        style=flex_center,
                                                        ), ],
                                             style=flex_center,
                                             ),
                                     dbc.Col([dbc.Checkbox(id='visible-select-all',
                                                           value=False,
                                                           persistence=True,
                                                           persistence_type='local',
                                                           style={'display': 'flex',
                                                                  'justify-content': 'end',
                                                                  'align-items': 'center'},
                                                           ), ],
                                             style=flex_center,
                                             ),
                                     dbc.Col([dbc.Checkbox(id='color-select-all',
                                                           value=False,
                                                           persistence=True,
                                                           persistence_type='local',
                                                           style={'display': 'flex',
                                                                  'justify-content': 'end',
                                                                  'align-items': 'center'},
                                                           ), ],
                                             style=flex_center,
                                             ), ],
                                    style={
                                        'margin-left': 0,
                                        'margin-right': 0,
                                        'width': SETTINGS_CONTAINER_WIDTH,
                                    },
                                    )
                            ],
                           fluid=True,
                           style={'justify-content': 'center',
                                  'display': 'block',
                                  'padding': 0,
                                  'width': SETTINGS_CONTAINER_WIDTH,
                                  }
                           )

    freeze_col_input = html.Div([dbc.Label(['Freeze Cols:'], style=label_style),
                                 dbc.Input(type="number", size='sm', min=0, step=1,
                                           id='freeze-cols',
                                           persistence=True,
                                           persistence_type='local',
                                           style={'width': 50}), ],
                                style=flex_center,
                                )

    sort_mode_input = html.Div([dbc.Label(['Sort Mode:'], style=label_style),
                                dbc.Select(options=[{'label': 'single', 'value': 'single'},
                                                    {'label': 'multi', 'value': 'multi'}],
                                           value='single',
                                           id='sort-mode',
                                           persistence=True,
                                           persistence_type='local',
                                           style={'width': 100}
                                           ), ],
                               style=flex_center,
                               )

    footer = dbc.Container([dbc.Row([dbc.Col([freeze_col_input],
                                             style=flex_center,
                                             ),
                                     dbc.Col([sort_mode_input],
                                             style=flex_center,
                                             ),
                                     ],
                                    style=flex_center,
                                    ),
                            dbc.Row([dbc.Col([dbc.Button('Apply',
                                                         id='settings-apply-btn',
                                                         size='sm', color='secondary', outline=True,
                                                         )], style=flex_center, )],
                                    style={'display': 'flex',
                                           'justify-content': 'center',
                                           'align-items': 'center', 'padding-top': 10, },
                                    )
                            ],
                           fluid=True,
                           )

    rows = []
    for idx, col in enumerate(columns):
        row = dbc.Col([dbc.Row([dbc.Col([dbc.Label(col, style=flex_center, id=col,)],
                                        style=flex_center,
                                        ),
                                dbc.Col([dbc.Checkbox(id=generate_id('visible', col),
                                                      value=False,
                                                      persistence=True,
                                                      persistence_type='local',
                                                      style=flex_center,
                                                      ), ],
                                        style=flex_center,
                                        ),
                                dbc.Col([dbc.Checkbox(id=generate_id('color', col),
                                                      value=False,
                                                      persistence=True,
                                                      persistence_type='local',
                                                      style=flex_center,
                                                      ), ],
                                        style=flex_center,
                                        ), ],
                               style={'display': 'flex',
                                      'justify-content': 'center',
                                      'align-items': 'center',
                                      'margin': 0,
                                      'width': SETTINGS_CONTAINER_WIDTH,
                                      },

                               ),
                       ],
                      id=generate_id('row', col),

                      )
        rows.append(row)

    menu = GridLayout(children=rows,
                      id='grid-menu',
                      ncols=1,
                      nrows=1,
                      gridCols=1,
                      width=SETTINGS_CONTAINER_WIDTH,
                      isResizable=False,
                      height=6,
                      # isBounded=True,
                      # verticalCompact=False,
                      # compactType='horizontal',
                      # useCSSTransforms=False,
                      autoSize=True,
                      # isDroppable=True,
                      # preventCollision=True,
                      margin=[0, 0],
                      containerPadding=[0, 0],
                      style={'justify-content': 'center',
                             'display': 'flex',
                             }

                      )

    modal_header = dbc.Container([header], fluid=True, style={'justify-content': 'center', })
    modal_body = dbc.Container([menu], fluid=True, style={'justify-content': 'center', })
    modal_footer = dbc.Container([footer], fluid=True, style={'justify-content': 'center', })

    settings = html.Div(
        [
            dbc.Button('Settings',
                       id='settings-modal-open-btn',
                       size='sm', color='secondary', outline=True,
                       ),

            dbc.Modal([dbc.ModalHeader([modal_header, cls_btn], style={'padding-bottom': 0}, close_button=False),
                       dbc.ModalBody([modal_body], ),
                       dbc.ModalFooter([modal_footer], style={'justify-content': 'center', }),
                       ],
                      id='settings-modal',
                      # keyboard=False,
                      scrollable=True,
                      backdrop=False,
                      is_open=False,
                      # centered=True,
                      # size="md",
                      # class_name
                      # style={'width': 380, },
                      ),

        ]
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
            'margin-left': 'auto', 'margin-right': 'auto',
            'padding-top': 12, 'padding-bottom': 12,
            'display': 'table',
        },
        fluid=True,
    )
    return col_defs, table_panel
