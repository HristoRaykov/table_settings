import copy

import QuantLib as ql
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, Input, Output, State, callback_context, html, dcc

from table_settings.constants import TABLE_WIDTH, TABLE_EXPAND_HEIGHT, TABLE_SHRINK_HEIGHT, ID_SEP
from table_settings.settings.settings_dash import settings_table_factory
from table_settings.table import table_panel_factory, BASE_TABLE_FORMAT
from table_settings.utils import generate_test_table, find_element_by_id, generate_id

pd.options.mode.chained_assignment = None

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 dbc.icons.BOOTSTRAP],

           )  # external_stylesheets=[dbc.themes.LITERA],

df = generate_test_table()

ids, def_cols, column_styles, def_table, def_setts, table_panel = table_panel_factory(df,
                                                                                      TABLE_WIDTH,
                                                                                      TABLE_EXPAND_HEIGHT)

color_scale_select = dcc.Dropdown(options=[{'label': 'Color Scale', 'value': 'color_scale'},
                                           {'label': 'Bars', 'value': 'bars'},
                                           {'label': 'Diverging Bars', 'value': 'div_bars'},
                                           ],
                                  value=None,
                                  )
app.layout = dbc.Container(children=[color_scale_select, table_panel],
                           id='debt_secs_layout',
                           style={'width': '100%',
                                  # 'max-width': '100%',
                                  'height': '96vh',
                                  },
                           fluid=True,

                           )

position_inputs = [Input(i, 'value') for i in ids['col_positions']]

visibility_outputs = [Output(i, 'value') for i in ids['col_visibilities']]
visibility_inputs = [Input(i, 'value') for i in ids['col_visibilities']]
visibility_states = [State(i, 'value') for i in ids['col_visibilities']]

color_outputs = [Output(i, 'value') for i in ids['col_colors']]
color_inputs = [Input(i, 'value') for i in ids['col_colors']]


@app.callback(
    Output(ids['table'], 'children'),
    Output(ids['settings'], 'children'),
    Output(ids['settings_store'], 'data'),
    Input(ids['settings_apply_btn'], 'n_clicks'),
    Input(ids['settings_reset_btn'], 'n_clicks'),
    State(ids['settings'], 'children'),
    State(ids['settings_store'], 'data'),
    State(ids['table'], 'children'),
)
def settings_apply(n_apply, n_reset, settings, settings_store, table):
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if trig_id == '' and settings_store:
        settings = settings_store


    if trig_id == ids['settings_reset_btn']:
        return def_table, def_setts.children, def_setts.children

    freez_cols = find_element_by_id(settings, ids['freeze_cols'])['props']['value']
    sort_mode = find_element_by_id(settings, ids['sort_mode'])['props']['value']
    col_settings = find_element_by_id(settings, ids['drag_container'])['props']['children']

    cols = []
    col_defs = []
    hidden_cols = []
    color_formats = copy.deepcopy(BASE_TABLE_FORMAT)

    for col in col_settings:
        col_id = col['props']['id']
        cols.append(col_id)

        col_def = def_cols[col_id]
        col_defs.append(col_def)

        visible = find_element_by_id(col, generate_id('visibility', col_id))['props']['value']
        if not visible:
            hidden_cols.append(col_id)

        # color = find_element_by_id(col, generate_id('color', col_id))['props']['value']
        # if color:
        # color_format = color_scale_styles.get(col_id)
        # color_format = div_bars.get(col_id)
        # if color_format:
        #     color_formats.extend(color_format)
        s = 5

    temp = df[cols]
    table['props']['columns'] = col_defs
    table['props']['data'] = temp.to_dict('records')
    table['props']['hidden_columns'] = hidden_cols
    table['props']['fixed_columns']['data'] = freez_cols
    table['props']['sort_mode'] = sort_mode
    table['props']['style_data_conditional'] = color_formats

    return table, settings, settings


@app.callback(
    Output(ids['drag_container'], 'children'),
    [position_inputs],
    State(ids['drag_container'], 'children'),
    prevent_initial_call=True,
)
def column_position(positions, columns):
    # cols = pd.Series([col['props']['id'] for col in columns])
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    trig_col_id = trig_id.split(ID_SEP)[-1]
    trig_col_idx = None
    for idx, col in enumerate(columns):
        col_id = col['props']['id']
        if col_id == trig_col_id:
            trig_col_idx = idx
            break

    col = columns.pop(trig_col_idx)
    pos_input = find_element_by_id(col, trig_id)
    insert_idx = pos_input['props']['value'] - 1
    columns.insert(insert_idx, col)

    # ordered = pd.Series([col['props']['id'] for col in columns])
    for idx, col in enumerate(columns, 1):
        position_input = col['props']['children']['props']['children'][1]['props']['children']['props']['children'][
            'props']
        position_input['value'] = idx

    return columns


@app.callback(
    Output(ids['visibility_select_all'], 'value'),
    [visibility_outputs],
    Input(ids['visibility_select_all'], 'value'),
    [visibility_inputs],
)
def visible_select_all(select_all, visibilities):
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if trig_id == ids['visibility_select_all']:
        count = len(visibilities)
        visibilities = [True] * count if select_all else [False] * count
    else:
        all_selected = all(visibilities)
        select_all = True if all_selected else False

    return select_all, visibilities


# @app.callback(
#     Output(ids['color_select_all'], 'value'),
#     [color_outputs],
#     Input(ids['color_select_all'], 'value'),
#     [color_inputs],
# )
# def color_select_all(select_all, colors):
#     trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
#
#     if trig_id == ids['color_select_all']:
#         count = len(colors)
#         colors = [True] * count if select_all else [False] * count
#     else:
#         all_selected = all(colors)
#         select_all = True if all_selected else False
#
#     return select_all, colors


if __name__ == '__main__':
    app.run_server(debug=True)
