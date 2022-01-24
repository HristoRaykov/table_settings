import pandas as pd
from dash_test import Dash, html, Output, Input, State, ClientsideFunction, callback_context
import dash_bootstrap_components as dbc

import QuantLib as ql

from drake.constants import CONDITIONAL_X_Y_GRAPH_TYPES
from drake.factory.factory import debt_secs_layout_factory, columns_by_type
from drake.factory.graph.axes import GRAPH_TYPES_MAP, X_AXIS, Y_AXIS
from drake.factory.graph.graph import graph_container_factory, figure_factory, graph_factory
from drake.factory.table import table_container
from drake.utils import ID_SEP
from research.container import YieldCurvesContainer

pd.options.mode.chained_assignment = None
ql.IborCoupon.createIndexedCoupons()

TABLE_CONTAINER_HEIGHT = '78%'
GRAPHS_CONTAINER_HEIGHT = '18%'

val_date = ql.Date(7, 1, 2021)
ql.Settings.instance().evaluationDate = val_date

container = YieldCurvesContainer(val_date)
debt_secs_table = container.debt_secs_table
debt_secs = debt_secs_table.get_table()

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, ],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.3/dragula.js",
                             'https://code.jquery.com/jquery-3.2.1.min.js'],
           )

ids = dict()

table_ids, table_panel = table_container(debt_secs)
ids['table'] = table_ids

cols = columns_by_type(debt_secs)
graph1_ids, graph_panel_1 = graph_container_factory(cols, prefix='graph_1')
ids['graph_1'] = graph1_ids

graph_panel_2 = dbc.Container(
    children=html.Div(id='result'),
    id='graph2_container',
    fluid=True,
)

app.layout = debt_secs_layout_factory(table_panel, graph_panel_1, graph_panel_2)
# app.layout = dbc.Container(
#     children=[table_panel, html.Div(id='result')],
#
#     style={'width': '85%', 'height': '100vh'},
#     fluid=True,
#
# )

# Table callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output(ids['table']['drag_container'], "data-drag"),
    [Input(ids['table']['drag_container'], "id")],
    [State(ids['table']['drag_container'], "children")],
)

axes_inputs = [Input(i, 'value') for i in ids['graph_1']['axes']]
visible_outputs = [Output(i, 'value') for i in ids['table']['col_visibilities']]
visible_inputs = [Input(i, 'value') for i in ids['table']['col_visibilities']]
color_outputs = [Output(i, 'value') for i in ids['table']['col_colors']]
color_inputs = [Input(i, 'value') for i in ids['table']['col_colors']]


@app.callback(
    Output('result', 'children'),
    Input(ids['table']['settings_apply_btn'], 'n_clicks'),
    Input(ids['table']['drag_container'], 'children'),
    prevent_initial_call=True,
)
def settings_apply(n, children):
    return ''


# @app.callback(
#     Output(ids['table']['visibility_select_all'], 'value'),
#     [visible_outputs],
#     Input(ids['table']['visibility_select_all'], 'value'),
#     [visible_inputs],
# )
# def visible_select_all(select_all, visibilities):
#     trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
#
#     if trig_id == ids['table']['visibility_select_all']:
#         count = len(visibilities)
#         visibilities = [True] * count if select_all else [False] * count
#     else:
#         all_selected = all(visibilities)
#         select_all = True if all_selected else False
#
#     return select_all, visibilities

# @app.callback(
#     Output(ids['table']['color_select_all'], 'value'),
#     [color_outputs],
#     Input(ids['table']['color_select_all'], 'value'),
#     [color_inputs],
# )
# def color_select_all(select_all, colors):
#     trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
#
#     if trig_id == ids['table']['color_select_all']:
#         count = len(colors)
#         colors = [True] * count if select_all else [False] * count
#     else:
#         all_selected = all(colors)
#         select_all = True if all_selected else False
#
#     return select_all, colors


# graph_1 callbacks
@app.callback(
    Output(ids['graph_1']['axes_ddm_store'], 'data'),
    axes_inputs,
    State(ids['graph_1']['axes_ddm'], 'children'),
    prevent_initial_call=True
)
def axes_change(*args):
    # save axes data on change
    ddm = args[-1]
    return ddm


@app.callback(
    Output(ids['graph_1']['full_scr_modal_body'], 'children'),
    Output(ids['graph_1']['full_scr_modal'], 'is_open'),
    Input(ids['graph_1']['full_scr_open_btn'], 'n_clicks'),
    Input(ids['graph_1']['full_scr_close_btn'], 'n_clicks'),
    State(ids['graph_1']['full_scr_modal'], 'is_open'),
    State(ids['graph_1']['graph_container'], 'children'),
    State(ids['graph_1']['full_scr_modal_body'], 'children'),
)
def toggle_full_scr_modal_1(n_full_scr_open_btn, n_full_scr_close_btn, is_open, graph, full_scr_graph):
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    children, open = [], None
    if trig_id == ids['graph_1']['full_scr_open_btn']:
        if n_full_scr_open_btn:
            open = not is_open
        else:
            open = is_open

        if open:
            children = graph

    elif trig_id == ids['graph_1']['full_scr_close_btn']:
        open = not is_open
        children = full_scr_graph

    return children, open


@app.callback(
    Output(ids['graph_1']['axes_ddm'], 'children'),
    Input(ids['graph_1']['graph_type'], 'value'),
    State(ids['graph_1']['axes_ddm'], 'children'),
    State(ids['graph_1']['axes_ddm_store'], 'data'),
)
def update_graph_axes_1(graph_type, axes, data):
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trig_id == '' and data:
        return data

    if not graph_type:
        visible = []
    else:
        visible = GRAPH_TYPES_MAP[graph_type]

    for d in axes:
        ax = d['props']
        try:
            name = ax['children'][1]['props']['id'].split(ID_SEP)[-1]
        except Exception as e:
            name = ax['children'][2]['props']['id'].split(ID_SEP)[-1]

        if name in visible:
            ax['style']['display'] = 'flex'
        else:
            ax['style']['display'] = 'none'

    return axes


@app.callback(
    Output(ids['graph_1']['axes'][0], 'multi'),
    Input(ids['graph_1']['x_multi'], 'value'),
)
def toggle_multi_select_x(multi):
    return multi


@app.callback(
    Output(ids['graph_1']['axes'][1], 'multi'),
    Input(ids['graph_1']['y_multi'], 'value'),
)
def toggle_multi_select_y(multi):
    return multi


@app.callback(
    Output(ids['graph_1']['graph_container'], 'children'),
    Input(ids['graph_1']['plot_btn'], 'n_clicks'),
    Input(ids['graph_1']['full_scr_close_btn'], 'n_clicks'),
    State(ids['graph_1']['graph_type'], 'value'),
    State(ids['graph_1']['axes_ddm'], 'children'),
    State(ids['graph_1']['full_scr_modal_body'], 'children'),
    State(ids['graph_1']['axes_ddm_store'], 'data'),
)
def plot_graph_1(n_plot_btn, n_full_scr_close_btn, graph_type, graph_axes, full_scr_graph, data):
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trig_id == ids['graph_1']['full_scr_close_btn']:
        return full_scr_graph

    if not graph_type:
        return html.Div('Select graph type')

    kwargs = dict()
    if trig_id == '':
        axes = data
    else:
        axes = graph_axes

    for axis in axes:
        ax = axis['props']
        try:
            name = ax['children'][1]['props']['id'].split(ID_SEP)[-1]
        except Exception as e:
            name = ax['children'][2]['props']['id'].split(ID_SEP)[-1]

        if name in GRAPH_TYPES_MAP[graph_type]:
            label = ax['children'][0]['props']['children'][0]
            optional = True if label.endswith('(opt.)') else False
            try:
                val = ax['children'][1]['props']['value']
            except Exception as e:
                val = None

            if not val and not optional:
                if graph_type in CONDITIONAL_X_Y_GRAPH_TYPES and name in [X_AXIS, Y_AXIS]:
                    pass
                else:
                    return html.Div('{} not selected'.format(name))

            kwargs[name] = val

    fig = figure_factory(debt_secs, graph_type=graph_type, **kwargs)
    graph = graph_factory(fig)

    return graph


if __name__ == '__main__':
    app.run_server(debug=True)
