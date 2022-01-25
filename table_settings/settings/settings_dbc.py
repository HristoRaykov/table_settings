import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc

from table_settings.constants import *
from table_settings.utils import generate_id


def settings_header_factory(prefix=None):
    visibility_id = generate_id(prefix, 'visibility')
    color_id = generate_id(prefix, 'color')

    settings_header = html.Thead([html.Div(html.Tr([html.Th(children='Column',
                                                            colSpan=1,
                                                            style={'width': COLUMNS_WIDTH,
                                                                   'padding': 1}),
                                                    html.Th(children='Position',
                                                            colSpan=1,
                                                            style={'width': POSITION_WIDTH,
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

                                                   )),
                                  html.Div(
                                      html.Tr([html.Th(children='select all',
                                                       colSpan=1,
                                                       style={'width': COLUMNS_WIDTH + POSITION_WIDTH,
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
                                  )
                                  ],
                                 style={'display': 'block', },
                                 )
    ids = {
        'visibility_select_all': visibility_id,
        'color_select_all': color_id,
    }

    return ids, settings_header


def column_setting_factory(name, position, max, prefix=None):
    col_id = generate_id(prefix, name)
    col_position_id = generate_id(prefix, 'position', name)
    col_visibility_id = generate_id(prefix, 'visibility', name)
    col_color_id = generate_id(prefix, 'color', name)

    # <div class="Select-input" style="display: inline-block;">

    color_picker = daq.ColorPicker(
        # id='my-color-picker-1',
        # label='Color Picker',
        # value=dict(hex='#119DFF')
    )
    # todo
    # colors = dbc.DropdownMenu(label='Select',
    #                           children=[color_picker
    #                               # dbc.DropdownMenuItem(color_picker),  # 'Color',
    #                               # dbc.DropdownMenuItem('Color Scale'),
    #                               # dbc.DropdownMenuItem('Bars'),
    #                               # dbc.DropdownMenuItem('Diverging Bars'),
    #                           ],
    #                           addon_type='append',
    #                           color='secondary',
    #                           size='sm',
    #                           id=col_color_id,
    #                           )
    color_scale_select = dcc.Dropdown(options=[{'label': 'Color Scale', 'value': 'color_scale'},
                                               {'label': 'Bars', 'value': 'bars'},
                                               {'label': 'Diverging Bars', 'value': 'div_bars'},
                                               ],
                                      value=None,
                                      # id=sort_mode_id,
                                      # persistence=True,
                                      # persistence_type='local',
                                      # size='sm',
                                      style={'width': 80}
                                      )
    row = html.Tr(
        html.Div(
            [
                html.Td(name, style={'width': COLUMNS_WIDTH}, ),
                html.Td(html.Div(dbc.Input(type="number",
                                           inputmode='numeric',
                                           id=col_position_id,
                                           size='sm',
                                           min=1,
                                           max=max,
                                           step=1,
                                           value=position,
                                           # persistence=True,
                                           # persistence_type='local',
                                           style={'width': 50, }, ),
                                 style={'display': 'flex',
                                        'justify-content': 'center',
                                        'align-items': 'center'},
                                 ),
                        style={'width': POSITION_WIDTH},
                        ),
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
                # chk_box = dbc.Checkbox(id=col_color_id,
                #                      value=False,
                #                      persistence=True,
                #                      persistence_type='local',
                #                      style={'display': 'flex',
                #                             'justify-content': 'center',
                #                             'align-items': 'center'},
                #                      )
                html.Td(color_scale_select,
                        style={'display': 'block','width': COLOR_WIDTH},
                        )
            ],

            style={'height': 35, 'overflow': 'hidden',
                   'display': 'flex',
                   'justify-content': 'center',
                   'align-items': 'center',
                   'padding': 0,
                   },
        ),
        id=col_id,
    )

    ids = {'col': name,
           'col_position': col_position_id,
           'col_visibility': col_visibility_id,
           'col_color': col_color_id,
           }

    return ids, row


def settings_table_factory(columns, prefix=None):
    rows = []
    ids = {'cols': [], 'col_positions': [], 'col_visibilities': [], 'col_colors': []}
    max_position = len(columns)
    for position, col in enumerate(columns, 1):
        row_ids, row = column_setting_factory(col, position, max_position, prefix=prefix)
        ids['cols'].append(row_ids['col'])
        ids['col_positions'].append(row_ids['col_position'])
        ids['col_visibilities'].append(row_ids['col_visibility'])
        ids['col_colors'].append(row_ids['col_color'])
        rows.append(row)

    drag_container_id = generate_id(prefix, 'drag_container')
    ids['drag_container'] = drag_container_id

    table_body = html.Tbody(rows,
                            id=drag_container_id,
                            style={
                                'overflow-y': 'scroll',
                                'display': 'block',
                                'max-height': SETTINGS_TABLE_HEIGHT,
                            }
                            )

    header_ids, settings_header = settings_header_factory(prefix)
    ids.update(header_ids)

    # todo html, dbc
    table = html.Table([settings_header, table_body],
                       # bordered=False,
                       # responsive=True,
                       # hover=True,
                       # striped=True,
                       # style={'display': 'block', },
                       )

    return ids, table


def settings_factory(columns, prefix=None):
    freeze_cols_id = generate_id(prefix, 'freeze_cols')
    sort_mode_id = generate_id(prefix, 'sort_mode')
    ids = {'freeze_cols': freeze_cols_id,
           'sort_mode': sort_mode_id,
           }

    sett_ids, table = settings_table_factory(columns, prefix=None)
    ids.update(sett_ids)

    freeze_col_input = dbc.Container(html.Div([dbc.Label(['Freeze Cols:'],
                                                         style={
                                                             'text-align': 'center',
                                                             # 'font-size': '1rem',
                                                             'margin-right': 5,
                                                             'margin-bottom': 0,
                                                         }
                                                         ),
                                               dbc.Input(type="number",
                                                         size='sm',
                                                         min=0,
                                                         step=1,
                                                         value=0,
                                                         id=freeze_cols_id,
                                                         persistence=True,
                                                         persistence_type='local',
                                                         style={'width': 50}), ],
                                              style={'display': 'flex',
                                                     'justify-content': 'center',
                                                     'align-items': 'center', }
                                              ),
                                     fluid=True,
                                     style={'display': 'flex',
                                            'justify-content': 'center',
                                            'align-items': 'center',
                                            'padding': 0, },
                                     )

    sort_mode_input = dbc.Container(html.Div([dbc.Label(['Sort Mode:'],
                                                        style={
                                                            'text-align': 'center',
                                                            # 'font-size': '1rem',
                                                            'margin-right': 5,
                                                            'margin-bottom': 0,
                                                        }
                                                        ),
                                              dbc.Select(options=[{'label': 'single', 'value': 'single'},
                                                                  {'label': 'multi', 'value': 'multi'}],
                                                         value='single',
                                                         id=sort_mode_id,
                                                         persistence=True,
                                                         persistence_type='local',
                                                         size='sm',
                                                         style={'width': 100}
                                                         ), ],
                                             style={'display': 'flex',
                                                    'justify-content': 'center',
                                                    'align-items': 'center', }
                                             ),
                                    fluid=True,
                                    style={'display': 'flex',
                                           'justify-content': 'center',
                                           'align-items': 'center',
                                           'padding': 0, },
                                    )

    settings_apply_btn_id = generate_id(prefix, 'settings_apply_btn')
    settings_reset_btn_id = generate_id(prefix, 'settings_reset_btn')
    ids['settings_apply_btn'] = settings_apply_btn_id
    ids['settings_reset_btn'] = settings_reset_btn_id

    apply_btn = dbc.Container(dbc.Button('Apply',
                                         id=settings_apply_btn_id,
                                         size='sm',
                                         color='secondary',
                                         # outline=True,
                                         ),
                              style={'display': 'flex', 'justify-content': 'center'}
                              )
    reset_btn = dbc.Container(dbc.Button('Defaults',
                                         id=settings_reset_btn_id,
                                         size='sm',
                                         color='danger',
                                         outline=True,
                                         ),
                              style={'display': 'flex', 'justify-content': 'center'}
                              )

    dd_container = dbc.Container([table,
                                  dbc.Container([freeze_col_input, sort_mode_input],
                                                fluid=True,
                                                style={'display': 'flex',
                                                       'justify-content': 'center',
                                                       'align-items': 'center',
                                                       'padding': 0,
                                                       'margin-left': 0, 'margin-right': 0,
                                                       'margin-top': 10, 'margin-bottom': 10,
                                                       }
                                                ),
                                  dbc.Container([reset_btn, apply_btn],
                                                fluid=True,
                                                style={'display': 'flex',
                                                       'justify-content': 'center',
                                                       'align-items': 'center',
                                                       'padding': 0,
                                                       'margin-left': 0, 'margin-right': 0,
                                                       'margin-top': 15, 'margin-bottom': 0,
                                                       }
                                                ),
                                  ],
                                 fluid=True,
                                 style={'display': 'block', 'justify-content': 'center', 'overflowY': 'auto'})
    settings_id = generate_id(prefix, 'settings')
    settings_close_btn_id = generate_id(prefix, 'settings_close_btn')
    ids['settings'] = settings_id
    ids['settings_close_btn'] = settings_close_btn_id

    settings = dbc.DropdownMenu(label="Settings",
                                children=dd_container,
                                color='secondary',
                                size='sm',
                                id=settings_id,
                                )

    return ids, settings
