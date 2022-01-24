import numpy as np
import dash_bootstrap_components as dbc
from dash_test import html

from web.dash.factory.graph.axes import COLS_MAP, NUM_COLS, ENUM_COLS, TEXT_COLS, BOOL_COLS, DATE_COLS, \
    ALL_COLS
from web.dash.utils import _is_enum_col


def columns_by_type(df):
    num_cols, enum_cols, text_cols, booln_cols, date_cols = [], [], [], [], []

    for col in df.columns:
        try:
            val = df[col].dropna().values[0]
        except Exception as e:
            # todo logging
            continue

        t = type(val)
        if np.issubdtype(t, np.float64) or np.issubdtype(t, np.int64):
            num_cols.append(col)
        elif np.issubdtype(t, np.datetime64):
            date_cols.append(col)
        elif np.issubdtype(t, np.bool):
            booln_cols.append(col)
        else:
            if _is_enum_col(df[col]):
                enum_cols.append(col)
            else:
                text_cols.append(col)

    cols = COLS_MAP.copy()
    cols[NUM_COLS] = num_cols
    cols[ENUM_COLS] = enum_cols
    cols[TEXT_COLS] = text_cols
    cols[BOOL_COLS] = booln_cols
    cols[DATE_COLS] = date_cols
    cols[ALL_COLS] = num_cols + enum_cols + text_cols + booln_cols + date_cols

    return cols


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

    layout = dbc.Container(
        children=[table, graph_container],
        id='debt_secs_layout',
        style={'width': '100%',
               'height': '96%',
               },
        fluid=True,

    )

    return layout
