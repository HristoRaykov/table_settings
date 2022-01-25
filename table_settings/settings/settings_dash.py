import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc

from table_settings.constants import *
from table_settings.utils import generate_id




def settings_table_factory(columns, prefix=None):



    return None


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
