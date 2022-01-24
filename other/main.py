import pandas as pd
from dash_test import callback_context, Dash, Output, Input, State, ClientsideFunction

from drake.constants import *
from drake.functions import *

pd.options.mode.chained_assignment = None

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
           )

rng = np.random.default_rng()

cols_count = 30
columns = ['col_' + str(i) for i in np.arange(1, cols_count + 1)]
data = rng.integers(0, 100, size=(100, cols_count))
df = pd.DataFrame(data, columns=columns)

col_defs, table = table_factory(df)
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
                           )

btn = dbc.Button('Apply',
                 id='settings-apply-btn',
                 size='sm', color='secondary', outline=True,
                 style={}, )

rows = []
for col in df.columns:
    row = dbc.Container([dbc.Row([dbc.Col([dbc.Label(col, style=flex_center, id=col, )],
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

# btn = dbc.Button('Btn', id='btn', size='sm', color='secondary', outline=True, )
menu = html.Div(id="drag_container", children=rows)
cls_btn = dbc.Button(class_name="btn-close",
                     id='settings-modal-close-btn',
                     style={'display': 'flex', 'justify-content': 'end', })

modal_header = dbc.Container([header], fluid=True, style={'justify-content': 'center', })
modal_body = dbc.Container(menu, fluid=True, style={'justify-content': 'center', })
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

settings_container = dbc.Container(children=[settings],
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
    id='table_container',
    children=[html.Div(id='settings',
                       children=settings_container,
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

app.layout = dbc.Container(
    children=[table_panel],

    style={'width': '100%', 'height': '100vh'},
    fluid=True,

)

# @app.callback(
#     Output("order", "children"),
#     [
#         Input(component_id="btn", component_property="n_clicks"),
#         Input(component_id="drag_container", component_property="children"),
#     ],
# )
# def watch_children(nclicks, children):
#     """Display on screen the order of children"""
#     return str(children)


cols = df.columns
visible_select_all_id = 'visible-select-all'
color_select_all_id = 'color-select-all'
# col_sett_ids = dict()
# for col in df.columns:
#     col_sett_ids[col] = {'visible': generate_id('visible', col),
#                          'color': generate_id('color', col)
#                          }
visible_ids = [generate_id('visible', c) for c in cols]
color_ids = [generate_id('color', c) for c in cols]

visible_outputs = [Output(i, 'value') for i in visible_ids]
visible_inputs = [Input(i, 'value') for i in visible_ids]
color_outputs = [Output(i, 'value') for i in color_ids]
color_inputs = [Input(i, 'value') for i in color_ids]

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [Input("drag_container", "id")],
    [State("drag_container", "children")],
) \
 \
 \
@app.callback(
    Output(visible_select_all_id, 'value'),
    [visible_outputs],
    Input(visible_select_all_id, 'value'),
    [visible_inputs],
)
def visible_select_all(select_all, visibilities):
    ctx = callback_context
    trig_id = ctx.triggered[0]['prop_id'].split('.')[0] = ctx.triggered[0]["prop_id"].split(".")[0]

    if trig_id == visible_select_all_id:
        count = len(visibilities)
        visibilities = [True] * count if select_all else [False] * count
    else:
        all_selected = all(visibilities)
        select_all = True if all_selected else False

    return select_all, visibilities


# @app.callback(
#     Output(color_select_all_id, 'value'),
#     [color_outputs],
#     Input(color_select_all_id, 'value'),
#     [color_inputs],
# )
# def color_select_all(select_all, colors):
#     ctx = callback_context
#     trig_id = ctx.triggered[0]['prop_id'].split('.')[0] = ctx.triggered[0]["prop_id"].split(".")[0]
#
#     if trig_id == color_select_all_id:
#         count = len(colors)
#         colors = [True] * count if select_all else [False] * count
#     else:
#         all_selected = all(colors)
#         select_all = True if all_selected else False
#
#     return select_all, colors


@app.callback(
    Output('settings-modal', 'is_open'),
    Output('table', 'children'),
    Input('settings-apply-btn', 'n_clicks'),
    Input('settings-modal-open-btn', 'n_clicks'),
    Input('settings-modal-close-btn', 'n_clicks'),
    State('table', 'children'),
    State('settings-modal', 'children'),
    # State('grid-menu', 'children'),
    State('settings-modal', 'is_open'),
    State("drag_container", "children"),
)
def settings_apply(n_apply, n_modal_open, n_modal_close, table, settings, is_open, drag_container):  # col_settings,
    ctx = callback_context
    trig_id = ctx.triggered[0]['prop_id'].split('.')[0] = ctx.triggered[0]["prop_id"].split(".")[0]

    if n_apply or n_modal_open or n_modal_close:
        is_open = not is_open

    if trig_id == 'settings-apply-btn':
        s = 5
        # todo apply settings to table
        # freeze_cols = find_element_by_id(settings, 'freeze-cols')
        # sort_mode = find_element_by_id(settings, 'sort-mode')
        # rows = find_element_by_id(settings, 'grid-menu')['props']['children']
        #
        # cols = []
        # col_defs = []
        # hidden_cols = []
        #
        # for row in rows:
        #     col = row['props']['id']
        #     cols.append(col)
        #
        #     col_def = col_defs_map[col]
        #     col_defs.append(col_def)
        #
        #     visible = find_element_by_id([row], generate_id('visible', col))['props']['value']
        #     if not visible:
        #         hidden_cols.append(col)
        #
        #     color = find_element_by_id([row], generate_id('color', col))['props']['value']

        s = 5

    temp = df[cols]
    # table['props']['columns'] = col_defs
    # table['props']['data'] = temp.to_dict('records')
    # table['props']['hidden_columns'] = hidden_cols
    s = 5

    return is_open, table


if __name__ == '__main__':
    app.run_server(debug=True)
