import dash_bootstrap_components as dbc
from dash import html
from plotly import express as px

from web.dash.constants import *
from web.dash.factory.graph.axes import graph_axes_factory
from web.dash.factory.graph.type import *
from web.dash.utils import generate_id


def graph_container_factory(cols, prefix=None):
    graph_type_id = generate_id(prefix, 'type')
    plot_btn_id = generate_id(prefix, 'plot_btn')
    full_scr_open_btn_id = generate_id(prefix, 'full_scr_open_btn')
    full_scr_close_btn_id = generate_id(prefix, 'full_scr_close_btn')
    full_scr_body_id = generate_id(prefix, 'full_scr_modal_body')
    full_scr_modal_id = generate_id(prefix, 'full_scr_modal')
    graph_container_id = generate_id(prefix, 'container')
    graph_panel_id = generate_id(prefix, 'panel')

    ids = {
        'graph_type': graph_type_id,
        # 'axes_settings': axes_id,
        'plot_btn': plot_btn_id,
        'full_scr_open_btn': full_scr_open_btn_id,
        'full_scr_close_btn': full_scr_close_btn_id,
        'full_scr_modal_body': full_scr_body_id,
        'full_scr_modal': full_scr_modal_id,
        'graph_container': graph_container_id,
        'graph_panel': graph_panel_id,
    }

    axes_ids, axes = graph_axes_factory(cols, prefix=prefix)
    ids.update(axes_ids)

    graph_panel = dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label(['Graph Type'],
                                      style={'margin-right': 10, }
                                      ),
                            html.Div(children=graph_type_factory(graph_type_id),
                                     style={'margin-right': 30, }
                                     ),

                            html.Div(children=[axes],
                                     # id=axes_id,
                                     style={'margin-right': 30, },
                                     ),
                            # html.Div(children=[dcc.Checklist(id=generate_id(page, 'graph_trendline', suffix),
                            #                                  options=[{'label': 'Trendline', 'value': 'ols'}],
                            #                                  persistence=True,
                            #                                  persistence_type='local',
                            #                                  value=['ols'],
                            #                                  style={'display': 'flex'}
                            #                                  )
                            #                    ],
                            #          style={'margin-right': 30, },
                            #          ),
                            html.Div(
                                dbc.Button('Plot',
                                           id=plot_btn_id,
                                           size='sm', color='secondary', outline=True,
                                           ),
                            ),
                        ],
                        style={'display': 'flex', 'align-items': 'center'},
                    ),

                    dbc.Col(
                        dbc.Button(class_name="bi bi-fullscreen",
                                   id=full_scr_open_btn_id,
                                   outline=True, ),
                        style={'display': 'flex', 'justify-content': 'end', 'max-width': 100, 'padding-left': 0},
                    ),

                ],
                align='center',
                # justify='between',
            ),
            dbc.Modal(children=[dbc.ModalHeader(dbc.Button(class_name="btn-close",
                                                           id=full_scr_close_btn_id,
                                                           style={'display': 'flex', 'justify-content': 'end', }),
                                                close_button=False,
                                                ),
                                dbc.ModalBody(html.Div(children=[],
                                                       id=full_scr_body_id,
                                                       style={'width': '100%', 'height': '100%'}), ),
                                ],
                      id=full_scr_modal_id,
                      is_open=False,
                      fullscreen=True,
                      ),
            dbc.Container(children=[],
                          id=graph_container_id,
                          style={'padding': 0}, ),
        ],
        id=graph_panel_id,
        fluid=True,
        style={'padding': 0},
    )

    return ids, graph_panel


def graph_factory(figure):
    graph = dcc.Graph(figure=figure,
                      style={'width': '100%', 'height': '100%',
                             'margin-left': 'auto', 'margin-right': 'auto', },
                      config={'displaylogo': False,
                              'scrollZoom': True,
                              'modeBarButtonsToRemove': [],  # 'zoom', 'pan'
                              'modeBarButtonsToAdd': ['drawline',
                                                      'drawopenpath',
                                                      'drawclosedpath',
                                                      'drawcircle',
                                                      'drawrect',
                                                      'eraseshape'
                                                      ],
                              },
                      )
    return graph


def figure_factory(df, graph_type, **kwargs):
    if graph_type == LINE_GRAPH:
        fig = px.line(df, **kwargs)
    elif graph_type == LINE_3D_GRAPH:
        fig = px.line_3d(df, **kwargs)
    elif graph_type == SCATTER_GRAPH:
        if kwargs.get('trendline') == 'ols':
            trendline_options = dict()
            neg_x = (df[kwargs.get('x')] < 0).any()
            neg_y = (df[kwargs.get('y')] < 0).any()
            if neg_x:
                trendline_options['log_x'] = False
            else:
                trendline_options['log_x'] = True

            if neg_y:
                trendline_options['log_y'] = False
            else:
                trendline_options['log_y'] = True
            kwargs['trendline_options'] = trendline_options
        if kwargs.get('trendline') == 'ewm':
            kwargs['trendline_options'] = {'alpha': 0.4, 'adjust': True}
        if kwargs.get('trendline') == 'rolling':
            kwargs['trendline_options'] = {'window': 14}
        fig = px.scatter(df, **kwargs)
    elif graph_type == SCATTER_3D_GRAPH:
        fig = px.scatter_3d(df, **kwargs)
    elif graph_type == HISTOGRAM_GRAPH:
        kwargs['barmode'] = 'group'
        fig = px.histogram(df, **kwargs)
    elif graph_type == CDF_GRAPH:
        fig = px.ecdf(df, **kwargs)
    elif graph_type == BAR_GRAPH:
        kwargs['barmode'] = 'group'
        fig = px.bar(df, **kwargs)
    elif graph_type == BOX_GRAPH:
        kwargs['points'] = 'all'
        fig = px.box(df, **kwargs)
    elif graph_type == VIOLIN_GRAPH:
        kwargs['points'] = 'all'
        kwargs['box'] = True
        fig = px.violin(df, **kwargs)

    else:
        fig = None

    return fig
