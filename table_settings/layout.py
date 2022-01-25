import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc


def debt_secs_layout_factory(table, graph1, graph2):
    graph_container = dbc.Container(
        [dbc.Accordion([dbc.AccordionItem([dbc.Row([dbc.Col(graph1, style={"max-width": '50%', }, ),
                                                    dbc.Col(graph2, style={"max-width": '50%', }, ),
                                                    ], ),
                                           ],
                                          title="Graphs"),
                        ],
                       id='debt_secs_accordion',
                       # flush=True,
                       active_item=None, )
         ],
        id='debt_secs_graphs_container',
        fluid=True,
    )
    color_scale_select = dcc.Dropdown(options=[{'label': 'Color Scale', 'value': 'color_scale'},
                                               {'label': 'Bars', 'value': 'bars'},
                                               {'label': 'Diverging Bars', 'value': 'div_bars'},
                                               ],
                                      value=None,
                                      # id=sort_mode_id,
                                      # persistence=True,
                                      # persistence_type='local',
                                      # size='sm',
                                      # style={'width': 100}
                                      )
    color_picker = daq.ColorPicker(
        # id='my-color-picker-1',
        # label='Color Picker',
        # value=dict(hex='#119DFF')
    )
    # todo
    colors = dbc.DropdownMenu(label='Select',
                              children=[color_picker
                                        # dbc.DropdownMenuItem(color_picker),  # 'Color',
                                        # dbc.DropdownMenuItem('Color Scale'),
                                        # dbc.DropdownMenuItem('Bars'),
                                        # dbc.DropdownMenuItem('Diverging Bars'),
                                        ],
                              addon_type='append',
                              color='secondary',
                              size='sm',
                              # id=col_color_id,
                              )

    layout = dbc.Container(
        children=[color_scale_select, table, graph_container],
        id='debt_secs_layout',
        style={'width': '100%',
               # 'max-width': '100%',
               'height': '96vh',
               },
        fluid=True,

    )

    return layout
