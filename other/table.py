import pandas as pd
from dash import Dash

from drake.functions import *

pd.options.mode.chained_assignment = None

rng = np.random.default_rng()

cols_count = 30
columns = ['col_' + str(i) for i in np.arange(1, cols_count + 1)]
# data = rng.integers(0, 100, size=(100, cols_count))
# df = pd.DataFrame(data, columns=columns)


# df = pd.DataFrame(
#     {
#         ('Visible', 'nodata'): {
#             'col_1': 'nodata',
#             'col_2': 'nodata',
#             'col_3': 'nodata',
#         },
#         ('Color Scale', 'nodata'): {
#             'col_1': 'nodata',
#             'col_2': 'nodata',
#             'col_3': 'nodata',
#         },
#     }
# )
# df.index.set_names('Columns', inplace=True)
# table = dbc.Table.from_dataframe(
#     df, striped=True, bordered=False, hover=True, index=True
# )


app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
           )

table_header = html.Thead([html.Tr([html.Th(children='Columns', colSpan=1, style={'width': COLUMNS_WIDTH}),
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
                          style={'display': 'block', }
                          )


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


rows = []
for col in columns:
    row = column_setting_factory(col)
    rows.append(row)

table_body = html.Tbody(rows,
                        id="drag_container",
                        style={
                            'overflow': 'auto',
                            'display': 'block',
                            # 'min-width': TABLE_WIDTH,
                            'max-height': '520px',
                        }
                        )

table = dbc.Table([table_header, table_body],
                  bordered=False,
                  # responsive=True,
                  # color='primary',
                  # size='sm',
                  hover=True,
                  striped=True,
                  style={'display': 'block', 'width': SETTINGS_TABLE_WIDTH}
                  )

dropdown = dbc.DropdownMenu(label="Settings",
                            children=[table,
                                      dbc.Button('Apply',
                                                 id='settings-apply-btn',
                                                 size='sm', color='secondary', outline=True,
                                                 )],

                            )

app.layout = dbc.Container(
    children=[
        # dropdown,
        table,
        html.Div(id='result'),
    ],
    style={'width': '80%', 'height': '50vh'},
    fluid=True,
)

# app.clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="make_draggable"),
#     Output("drag_container", "data-drag"),
#     [Input("drag_container", "id")],
#     [State("drag_container", "children")],
# )
#
#
# @app.callback(
#     Output('result', 'children'),
#     Input('settings-apply-btn', 'n_clicks'),
#     Input("drag_container", "children"),
#     # State("drag_container", "children"),
# )
# def settings_apply(n, children):
#     return ''


if __name__ == '__main__':
    app.run_server(debug=True)
