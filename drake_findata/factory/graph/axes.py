import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_daq as daq

from web.dash.constants import *

from web.dash.utils import generate_id, ID_SEP

NUM_COLS = 'num_cols'
ENUM_COLS = 'enum_cols'
TEXT_COLS = 'test_cols'
BOOL_COLS = 'bool_cols'
DATE_COLS = 'date_cols'
ALL_COLS = 'all_cols'

COLS_MAP = {
    NUM_COLS: [],
    ENUM_COLS: [],
    TEXT_COLS: [],
    BOOL_COLS: [],
    DATE_COLS: [],
    ALL_COLS: [],
}

X_AXIS = 'x'
Y_AXIS = 'y'
Z_AXIS = 'z'
COLOR = 'color'
SYMBOL = 'symbol'
SIZE = 'size'
HOVER_NAME = 'hover_name'
HOVER_DATA = 'hover_data'
FACET_ROW = 'facet_row'
FACET_COL = 'facet_col'
TEXT = 'text'
LINE_GROUP = 'line_group'
ORIENTATION = 'orientation'
HISTNORM = 'histnorm'
HISTFUNC = 'histfunc'
TRENDLINE = 'trendline'

AXES = {X_AXIS: {'cols': 'all', 'default': None, 'label': 'X Axis', 'multi': None, 'clearable': True, },
        Y_AXIS: {'cols': 'all', 'default': None, 'label': 'Y Axis', 'multi': None, 'clearable': True, },
        Z_AXIS: {'cols': 'all', 'default': None, 'label': 'Z Axis', 'multi': False, 'clearable': True, },
        COLOR: {'cols': 'all', 'default': None, 'label': 'Color (opt.)', 'multi': False, 'clearable': True, },
        SYMBOL: {'cols': 'all', 'default': None, 'label': 'Symbol (opt.)', 'multi': False, 'clearable': True, },
        SIZE: {'cols': 'all', 'default': None, 'label': 'Size (opt.)', 'multi': False, 'clearable': True, },
        HOVER_NAME: {'cols': 'all', 'default': None, 'label': 'Hover Name (opt.)', 'multi': False,
                     'clearable': True, },
        HOVER_DATA: {'cols': 'all', 'default': None, 'label': 'Hover Data (opt.)', 'multi': True, 'clearable': True, },
        FACET_ROW: {'cols': 'all', 'default': None, 'label': 'Facet Row (opt.)', 'multi': False, 'clearable': True, },
        FACET_COL: {'cols': 'all', 'default': None, 'label': 'Facet Col (opt.)', 'multi': False, 'clearable': True, },
        TEXT: {'cols': 'all', 'default': None, 'label': 'Text (opt.)', 'multi': False, 'clearable': True, },
        LINE_GROUP: {'cols': 'all', 'default': None, 'label': 'Line Group (opt.)', 'multi': False,
                     'clearable': True, },

        HISTNORM: {'cols': 'fixed', 'options': ['percent', 'probability', 'density', 'probability density'],
                   'default': None, 'label': 'Histnorm (opt.)', 'multi': False, 'clearable': True, },
        HISTFUNC: {'cols': 'fixed', 'options': ['count', 'sum', 'avg', 'min', 'max'], 'default': 'count',
                   'label': 'Histfunc', 'multi': False, 'clearable': False, },
        ORIENTATION: {'cols': 'fixed', 'options': ['v', 'h'], 'default': 'v', 'label': 'Orientation', 'multi': False,
                      'clearable': False, },
        TRENDLINE: {'cols': 'fixed', 'options': ['ols', 'lowess', 'expanding', 'ewm', 'rolling'], 'default': None,
                    'label': 'Trendline (opt.)', 'multi': False, 'clearable': True, },
        }

GRAPH_TYPES_MAP = {
    LINE_GRAPH: [X_AXIS, Y_AXIS, COLOR, SYMBOL, HOVER_NAME, HOVER_DATA, FACET_ROW, FACET_COL, TEXT, LINE_GROUP],
    LINE_3D_GRAPH: [X_AXIS, Y_AXIS, Z_AXIS, COLOR, SYMBOL, HOVER_NAME, HOVER_DATA, FACET_ROW, FACET_COL, TEXT,
                    LINE_GROUP],
    SCATTER_GRAPH: [X_AXIS, Y_AXIS, COLOR, SYMBOL, SIZE, HOVER_NAME, HOVER_DATA, TEXT, TRENDLINE],
    SCATTER_3D_GRAPH: [X_AXIS, Y_AXIS, Z_AXIS, COLOR, SYMBOL, SIZE, TEXT, HOVER_NAME, HOVER_DATA],

    HISTOGRAM_GRAPH: [X_AXIS, Y_AXIS, COLOR, FACET_ROW, FACET_COL, HOVER_NAME, HOVER_DATA, HISTNORM, HISTFUNC,
                      ORIENTATION],  # 'pattern_shape'
    CDF_GRAPH: [X_AXIS, Y_AXIS, COLOR, TEXT, SYMBOL, FACET_ROW, FACET_COL, HOVER_NAME, HOVER_DATA, ORIENTATION],
    BAR_GRAPH: [X_AXIS, Y_AXIS, COLOR, FACET_ROW, FACET_COL, HOVER_NAME, HOVER_DATA, TEXT, ORIENTATION],
    # 'pattern_shape'
    BOX_GRAPH: [X_AXIS, Y_AXIS, COLOR, FACET_ROW, FACET_COL, HOVER_NAME, HOVER_DATA, ORIENTATION],
    VIOLIN_GRAPH: [X_AXIS, Y_AXIS, COLOR, FACET_ROW, FACET_COL, HOVER_NAME, HOVER_DATA, ORIENTATION],

    # DISTPLOT_GRAPH: [],

}


def dropdown_factory(id, cols, default, label, multi, clearable):
    # lbl = dbc.Label([label],
    #                  style={
    #                      'min-width': 120,
    #                      "text-align": "center",
    #                      'margin-left': 10, 'margin-right': 10,
    #                      'margin-top': 'auto', 'margin-bottom': 'auto'
    #                  })

    ids = dict()
    if multi is None:
        # no size
        # multi_input = daq.BooleanSwitch(id=generate_id(id, 'multi'),
        #                                 on=False,
        #                                 label="Multi",
        #                                 persistence=True,
        #                                 persistence_type='local',
        #                                 labelPosition="top"
        #                                 )
        axis = id.split(ID_SEP)[-1]
        multi_input_id = generate_id(id, 'multi')
        k = axis + '_multi'
        ids[k] = multi_input_id

        multi_input = daq.ToggleSwitch(multi_input_id,
                                       # label="Multi",
                                       # labelPosition="top",
                                       value=False,
                                       vertical=True,
                                       size=25,
                                       persistence=True,
                                       persistence_type='local',
                                       )
        lbl = dbc.Label([label, multi_input],
                        # title='Toggle Multi Select',
                        style={
                            'display': 'flex',
                            'font-size': '0.9rem',
                            'justify-content': 'end',
                            'min-width': 120,
                            "text-align": "center",
                            'margin-left': 10, 'margin-right': 10,
                            'margin-top': 'auto', 'margin-bottom': 'auto'
                        })
        dd = html.Div([lbl,
                       dcc.Dropdown(id=id,
                                    options=[{'label': c, 'value': c} for c in cols],
                                    multi=False,
                                    clearable=clearable,
                                    persistence=True,
                                    persistence_type='local',
                                    value=default,
                                    style={'margin-right': 10,
                                           'width': 140, 'min-width': 140,
                                           },
                                    ),
                       ],
                      style={
                          'display': 'flex',
                          'justify-content': 'end', 'align-items': 'center',
                          'margin-top': 5, 'margin-bottom': 5
                      }
                      )
    else:
        lbl = dbc.Label([label],
                        style={
                            'min-width': 120,
                            "text-align": "center",
                            'font-size': '0.9rem',
                            'margin-left': 10, 'margin-right': 10,
                            'margin-top': 'auto', 'margin-bottom': 'auto'
                        })
        dd = html.Div([lbl,
                       dcc.Dropdown(
                           id=id,
                           options=[{'label': c, 'value': c} for c in cols],
                           multi=multi,
                           clearable=clearable,
                           persistence=True,
                           persistence_type='local',
                           value=default,
                           style={'margin-right': 10,
                                  'width': 140, 'min-width': 140,
                                  },
                       ),
                       ],
                      style={
                          'display': 'flex',
                          'justify-content': 'end', 'align-items': 'center',
                          'margin-top': 10, 'margin-bottom': 10
                      }
                      )

    return ids, dd


def dropdown_menu_factory(prefix, children):
    ddm_id = generate_id(prefix, 'ddm')
    ddm_store_id = generate_id(prefix, 'ddm_store')
    ddm = html.Div(
        [dbc.DropdownMenu(label='Select Axes...',
                          id=ddm_id,
                          children=children,
                          align_end=True,
                          color='secondary',
                          direction='down',
                          ),
         dcc.Store(id=ddm_store_id, storage_type='local'),
         ]
    )

    ids = {'axes_ddm': ddm_id, 'axes_ddm_store': ddm_store_id}

    return ids, ddm


def graph_axes_factory(cols, prefix):
    ids = dict()

    dds = []
    axes_ids = []
    for axis, options in AXES.items():
        axis_id = generate_id(prefix, axis)
        axes_ids.append(axis_id)
        axis_cols = options['cols']
        default = options['default']
        label = options['label']
        multi = options['multi']
        clearable = options['clearable']
        dd_options = []
        if axis_cols:
            if axis_cols == 'fixed':
                dd_options = options['options']
            elif axis_cols == 'all':
                dd_options = cols[ALL_COLS]
            else:
                for c in axis_cols:
                    dd_options.extend(cols[c])

        dd_ids, dd = dropdown_factory(axis_id, dd_options, default, label, multi, clearable)
        ids.update(dd_ids)
        dds.append(dd)

    ddm_ids, ddm = dropdown_menu_factory(prefix, dds)
    ids.update(ddm_ids)

    ids['axes'] = axes_ids

    return ids, ddm
