import QuantLib as ql
import dash_bootstrap_components as dbc
import pandas as pd
from dash_test import Dash, Input, Output, State, callback_context, html, no_update, ClientsideFunction

from research.container import YieldCurvesContainer
from web.dash.constants import CONDITIONAL_X_Y_GRAPH_TYPES
from web.dash.factory.factory import columns_by_type, debt_secs_layout_factory
from web.dash.factory.graph.axes import graph_axes_factory, GRAPH_TYPES_MAP, AXES, X_AXIS, Y_AXIS
from web.dash.factory.graph.graph import graph_container_factory, graph_factory, figure_factory
from web.dash.factory.table import table_factory, table_container
from web.dash.utils import *

pd.options.mode.chained_assignment = None
ql.IborCoupon.createIndexedCoupons()

PAGE = 'debt_secs'

TABLE_CONTAINER_HEIGHT = '78%'
GRAPHS_CONTAINER_HEIGHT = '18%'

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 dbc.icons.BOOTSTRAP],
           external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.3/dragula.js',
                             'https://code.jquery.com/jquery-3.2.1.min.js'],
           )  # external_stylesheets=[dbc.themes.LITERA],

# val_date = ql.Date(30, 12, 2021)
val_date = ql.Date(7, 1, 2021)
ql.Settings.instance().evaluationDate = val_date

container = YieldCurvesContainer(val_date)
debt_secs_table = container.debt_secs_table
debt_secs = debt_secs_table.get_table()

debt_secs = debt_secs.append(debt_secs)

# col_defs = column_definitions(debt_secs)

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

axes_inputs = [Input(i, 'value') for i in ids['graph_1']['axes']]

visibility_ids = [ids['table']['visibility_select_all'], *ids['table']['col_visibilities']]
visibility_outputs = [Output(i, 'value') for i in visibility_ids]
visibility_inputs = [Input(i, 'value') for i in visibility_ids]
visibility_states = [State(i, 'value') for i in visibility_ids]

color_ids = [ids['table']['color_select_all'], *ids['table']['col_colors']]
color_outputs = [Output(i, 'value') for i in color_ids]
color_inputs = [Input(i, 'value') for i in color_ids]

#
# @app.callback(
#     Output('debt_secs-layout', 'children'),
#     Input('debt_secs-table_container', 'data'),
#     State('debt_secs-layout', 'children'),
# )
# def table(accordion, app_layout):
#     spreadsheet_menu = find_element_by_id(app_layout, 'dash_test-spreadsheet-menu')
#     table_container = find_element_by_id(app_layout, 'debt_secs-table_container')
#     return no_update


# Table callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output(ids['table']['drag_container'], "data-drag"),
    [Input(ids['table']['drag_container'], "id")],
    [State(ids['table']['drag_container'], "children")],
)


@app.callback(
    Output(ids['table']['table'], 'children'),
    Output(ids['table']['settings'], 'children'),
    Input('debt_secs_accordion', 'active_item'),
    Input(ids['table']['settings_apply_btn'], 'n_clicks'),
    # Input(ids['table']['visibility_select_all'], 'value'),
    # [visibility_inputs],
    State(ids['table']['settings'], 'children'),
    State(ids['table']['table'], 'children'),
    prevent_initial_call=True,
)
def settings_apply(active_item, n_apply,  settings, table):  # col_settings, settings, table,visibilities,
    trig_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # table = find_element_by_id(table_container, ids['table']['table'])
    # settings = find_element_by_id(table_container, ids['table']['settings'])
    if trig_id == 'debt_secs_accordion':
        # if active_item:
        #     table['props']['css'][1]['rule'] = 'max-height: 35vh;'
        # else:
        #     table['props']['css'][1]['rule'] = 'max-height: 80vh;'

        return table #, settings

    # if trig_id in visibility_ids:
        # if trig_id == ids['table']['visibility_select_all']:
        #     select_all = visibilities[0]
        #     visibility = True if select_all else False
            # cols = find_element_by_id(settings, ids['table']['drag_container'])['props']['children']
            # for col in cols:
            #     name = col['props']['id']
            #     col_visibility_id = generate_id('visibility', name)
            #     col_visibility = find_element_by_id(col, col_visibility_id)
            #     col_visibility['props']['value'] = visibility

        # select_all = visibilities[0]
        # col_visibilities = visibilities[1:]
        # if trig_id == ids['table']['visibility_select_all']:
        #     count = len(visibilities)
        #     col_visibilities = [True] * count if select_all else [False] * count
        #     s = 5
        # else:
        #     v = visibilities[1:]
        #     all_selected = all(visibilities[1:])
        #     select_all = True if all_selected else False
        #     s = 5

        # return table, settings

    if trig_id == ids['table']['settings_apply_btn']:
        # todo apply settings to table
        cols = find_element_by_id(settings, ids['table']['drag_container'])['props']['children']
        # cols = find_element_by_id(settings['props']['children'], 'drag_container')['props']['children']

        #
        # cols = []
        # col_defs = []
        # hidden_cols = []
        #
        # for row in rows:
        #     col = row['props']['id']
        #     cols.append(col)
        #
        #     # col_def = col_defs_map[col]
        #     # col_defs.append(col_def)
        #
        #     visible = find_element_by_id([row], generate_id('visible', col))['props']['value']
        #     if not visible:
        #         hidden_cols.append(col)
        #
        #     color = find_element_by_id([row], generate_id('color', col))['props']['value']
        #
        #     s = 5
        #
        # temp = debt_secs[cols]
        # table['props']['columns'] = col_defs
        # table['props']['data'] = temp.to_dict('records')
        # table['props']['hidden_columns'] = hidden_cols
        s = 5

    return table#, settings


# @app.callback(
#     visibility_outputs,
#     Input(ids['table']['visibility_select_all'], 'value'),
#     [visibility_states],
#     prevent_initial_call=True,
# )
# def visible_select_all(select_all, visibilities):
#     count = len(visibilities)
#     visibilities = [True] * count if select_all else [False] * count
#
#     return visibilities


# @app.callback(
#     Output(ids['table']['visibility_select_all'], 'value'),
#     [visibility_outputs],
#     Input(ids['table']['visibility_select_all'], 'value'),
#     [visibility_inputs],
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


# @app.callback(
#     Output('result', 'children'),
#     Input(ids['table']['settings_apply_btn'], 'n_clicks'),
#     Input(ids['table']['drag_container'], 'children'),
#     Input('order', 'children'),
#     Input('reorder_btn', 'value'),
#     Input('debt_secs_layout', 'children'),
#     prevent_initial_call=True,
# )
# def settings_apply(n, children, order, btn_val, dom):
#     return ''


# Graph callbacks
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
