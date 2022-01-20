from dash import dcc

from web.dash.factory.graph.axes import GRAPH_TYPES_MAP
from web.dash.utils import generate_id


def graph_type_factory(id):
    dd = dcc.Dropdown(
        id=id,
        options=[{'label': g, 'value': g} for g in GRAPH_TYPES_MAP.keys()],
        # value=graph_types[0],
        # placeholder='Graph...',
        # clearable=False,
        persistence=True,
        persistence_type='local',
        style={
            'min-width': 140,
        }
    )

    return dd
