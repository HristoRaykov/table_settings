import pandas as pd
from dash_test import callback_context, Dash, Output, Input, State

from drake.functions import *

pd.options.mode.chained_assignment = None

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 dbc.icons.BOOTSTRAP])
rng = np.random.default_rng()

cols_count = 30
columns = ['col_' + str(i) for i in np.arange(1, cols_count + 1)]
data = rng.integers(0, 100, size=(100, cols_count))
df = pd.DataFrame(data, columns=columns)

# dash_draggable.DashboardItem
# dash_draggable.DraggableDashboard
# dash_draggable.DraggableDashboard


col_defs_map, table_container = table_container(df)

app.layout = dbc.Container(
    children=[table_container],

    style={'width': '100%', 'height': '100vh'},
    fluid=True,

)

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


@app.callback(
    Output(visible_select_all_id, 'value'),
    [visible_outputs],
    Input(visible_select_all_id, 'value'),
    [visible_inputs],
)
def visible_select_all(select_all, visibilities):
    ctx = callback_context
    trig_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trig_id == visible_select_all_id:
        count = len(visibilities)
        visibilities = [True] * count if select_all else [False] * count
    else:
        all_selected = all(visibilities)
        select_all = True if all_selected else False

    return select_all, visibilities


@app.callback(
    Output(color_select_all_id, 'value'),
    [color_outputs],
    Input(color_select_all_id, 'value'),
    [color_inputs],
)
def color_select_all(select_all, colors):
    ctx = callback_context
    trig_id = ctx.triggered[0]['prop_id'].split('.')[0] = ctx.triggered[0]["prop_id"].split(".")[0]

    if trig_id == color_select_all_id:
        count = len(colors)
        colors = [True] * count if select_all else [False] * count
    else:
        all_selected = all(colors)
        select_all = True if all_selected else False

    return select_all, colors


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
)
def settings_apply(n_apply, n_modal_open, n_modal_close, table, settings,  is_open): # col_settings,
    ctx = callback_context
    trig_id = ctx.triggered[0]['prop_id'].split('.')[0] = ctx.triggered[0]["prop_id"].split(".")[0]

    if n_apply or n_modal_open or n_modal_close:
        is_open = not is_open

    if trig_id == 'settings-apply-btn':
        # todo apply settings to table
        freeze_cols = find_element_by_id(settings, 'freeze-cols')
        sort_mode = find_element_by_id(settings, 'sort-mode')
        rows = find_element_by_id(settings, 'grid-menu')['props']['children']

        cols = []
        col_defs = []
        hidden_cols = []

        for row in rows:
            col = row['props']['id']
            cols.append(col)

            col_def = col_defs_map[col]
            col_defs.append(col_def)

            visible = find_element_by_id([row], generate_id('visible', col))['props']['value']
            if not visible:
                hidden_cols.append(col)

            color = find_element_by_id([row], generate_id('color', col))['props']['value']

            s = 5

        temp = df[cols]
        # table['props']['columns'] = col_defs
        # table['props']['data'] = temp.to_dict('records')
        # table['props']['hidden_columns'] = hidden_cols
        s = 5

    return is_open, table


# @app.callback(
#     Output('settings-modal', 'is_open'),
#     [Input('settings-modal-open-btn', 'n_clicks'), Input('settings-modal-close-btn', 'n_clicks')],
#     [State('settings-modal', 'is_open')],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
