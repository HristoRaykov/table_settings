ID_SEP = '-'

LINE_GRAPH = 'line'
LINE_3D_GRAPH = 'line_3d'
SCATTER_GRAPH = 'scatter'
SCATTER_3D_GRAPH = 'scatter_3d'
HISTOGRAM_GRAPH = 'histogram'
CDF_GRAPH = 'ecdf'
BAR_GRAPH = 'bar'
BOX_GRAPH = 'box'
VIOLIN_GRAPH = 'violin'
DISTPLOT_GRAPH = 'distplot'

CONDITIONAL_X_Y_GRAPH_TYPES = [HISTOGRAM_GRAPH, CDF_GRAPH, BAR_GRAPH, BOX_GRAPH, VIOLIN_GRAPH]

table_id_keys = ['table', 'settings', 'settings_store', 'settings_close_btn', 'table_container',
                 'visibility_select_all', 'color_select_all',
                 'cols', 'col_positions', 'col_visibilities', 'col_colors',
                 'drag_container',
                 'freeze_cols', 'sort_mode', 'settings_apply_btn', 'settings_reset_btn'
                 ]

graph_id_keys = ['graph_type', 'plot_btn', 'full_scr_open_btn', 'full_scr_close_btn',
                 'full_scr_modal', 'full_scr_modal_body',
                 'graph_container', 'graph_panel',
                 'axes', 'axes_ddm', 'axes_ddm_store',
                 'x_multi', 'y_multi',

                 ]

COLUMNS_WIDTH = 150
POSITION_WIDTH = 60
VISIBLE_WIDTH = 100
COLOR_WIDTH = 100
SETTINGS_TABLE_WIDTH = COLUMNS_WIDTH + POSITION_WIDTH + VISIBLE_WIDTH + COLOR_WIDTH
SETTINGS_TABLE_HEIGHT = '77vh'
TABLE_WIDTH = '97.5vw'

TABLE_EXPAND_HEIGHT = '80vh'
TABLE_SHRINK_HEIGHT = '35vh'


LEFT_TAIL_TEXT_COLOR_PERCENTILE = 10
RIGHT_TAIL_TEXT_COLOR_PERCENTILE = 80