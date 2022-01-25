import numpy as np
from matplotlib import dates as mdates, colors, pyplot as plt

from table_settings.constants import LEFT_TAIL_TEXT_COLOR_PERCENTILE, RIGHT_TAIL_TEXT_COLOR_PERCENTILE

PLT_CMAP = plt.cm.get_cmap('RdYlGn')


def _data_bars(series):
    column = series.name
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [((series.max() - series.min()) * i) + series.min() for i in bounds]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            # colorс #0074D9, rgb(189, 215, 231)
            'background': (
                """
                    linear-gradient(90deg,
                    rgb(189, 215, 231) 0%,
                    rgb(189, 215, 231) {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


def _data_bars_diverging(series, color_above='#3D9970', color_below='#FF4136'):
    column = series.name
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    col_max = series.max()
    col_min = series.min()
    ranges = [((col_max - col_min) * i) + col_min for i in bounds]
    midpoint = (col_max + col_min) / 2.

    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        min_bound_percentage = bounds[i - 1] * 100
        max_bound_percentage = bounds[i] * 100

        style = {
            'if': {
                'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'paddingBottom': 2,
            'paddingTop': 2
        }
        if max_bound > midpoint:
            background = (
                """
                    linear-gradient(90deg,
                    white 0%,
                    white 50%,
                    {color_above} 50%,
                    {color_above} {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(
                    max_bound_percentage=max_bound_percentage,
                    color_above=color_above
                )
            )
        else:
            background = (
                """
                    linear-gradient(90deg,
                    white 0%,
                    white {min_bound_percentage}%,
                    {color_below} {min_bound_percentage}%,
                    {color_below} 50%,
                    white 50%,
                    white 100%)
                """.format(
                    min_bound_percentage=min_bound_percentage,
                    color_below=color_below
                )
            )
        style['background'] = background
        styles.append(style)

    return styles


def bar_styles(df):
    bar_map = dict()
    for col in df.columns:
        t = df[col].dtype
        if t == np.float64 or t == np.int64:  # np.issubdtype(t, np.datetime64) or
            s = _data_bars(df[col])
            bar_map[col] = s

    return bar_map


def diver_bar_styles(df):
    bar_map = dict()
    for col in df.columns:
        t = df[col].dtype
        if t == np.float64 or t == np.int64:  # np.issubdtype(t, np.datetime64) or
            s = _data_bars_diverging(df[col])
            bar_map[col] = s

    return bar_map


def _color_scale_map(df):
    color_map = dict()
    for col in df.columns:
        s = df[col].dropna().unique()
        t = df[col].dtype

        if t == np.float64 or t == np.int64 or np.issubdtype(t, np.datetime64):
            if np.issubdtype(t, np.datetime64):
                vals = [mdates.date2num(v) for v in s]
                text_color_down = np.percentile(s, LEFT_TAIL_TEXT_COLOR_PERCENTILE)
                text_color_up = np.percentile(s, RIGHT_TAIL_TEXT_COLOR_PERCENTILE)
            else:
                vals = s
                text_color_down = np.percentile(vals, LEFT_TAIL_TEXT_COLOR_PERCENTILE)
                text_color_up = np.percentile(vals, RIGHT_TAIL_TEXT_COLOR_PERCENTILE)

            min_val = np.percentile(vals, 2)
            mean_val = np.percentile(vals, 50)
            max_val = np.percentile(vals, 98)
            if min_val < mean_val < max_val:
                # norm = colors.Normalize(min_val, max_val)
                norm = colors.TwoSlopeNorm(vmin=min_val, vcenter=mean_val, vmax=max_val)
                m = dict()
                colors_list = PLT_CMAP(norm(vals))

                for val, c in zip(s, colors_list):
                    if val < text_color_down or val > text_color_up:
                        text_color = 'white'
                    else:
                        text_color = 'black'
                    m[val] = (colors.to_hex(c.flatten()), text_color)

                color_map[col] = m

    return color_map


def color_scale_styles(debt_secs):
    color_scale_map = _color_scale_map(debt_secs)
    color_scale_styles = dict()
    for col, colors_dic in color_scale_map.items():
        col_filters = []
        for val, (bg_color, text_color) in colors_dic.items():
            if np.issubdtype(val, np.datetime64):
                d = str(val)[:10]
                filter_query = '{{{}}} datestartswith "{}"'.format(col, d)

            else:
                filter_query = '{{{}}} = {}'.format(col, val)

            f = {
                'if': {
                    'column_id': col,
                    'filter_query': filter_query,
                },
                'backgroundColor': bg_color,
                'color': text_color
            }
            col_filters.append(f)

        color_scale_styles[col] = col_filters

    return color_scale_styles


def styles_factory(df):
    color_scales = color_scale_styles(df)
    bars = bar_styles(df)
    div_bars = diver_bar_styles(df)
    column_styles = {'color_scales': color_scales,
                     'bars': bars,
                     'div_bars': div_bars,
                     }

    return column_styles
