import QuantLib as ql
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.figure_factory as ff
import plotly.express.trendline_functions
import plotly.graph_objects as go

from research.container import YieldCurvesContainer

pd.options.mode.chained_assignment = None

val_date = ql.Date(30, 12, 2021)
ql.Settings.instance().evaluationDate = val_date

container = YieldCurvesContainer(val_date)
debt_secs_table = container.debt_secs_table
debt_secs = debt_secs_table.get_table()

# debt_secs = debt_secs.dropna()

# fig = px.line(debt_secs,
#               x='symbol',
#               y=['price\u0394\u0025', 'price'],
#               # color='rate_type',
#               symbol=None,
#               hover_name='symbol',
#               hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#               text='symbol',
#               # line_group='rate_type',
#               # markers=True,
#               )

# fig = px.line_3d(debt_secs,
#                  x='symbol',
#                  y='price\u0394\u0025',
#                  z='price',
#                  color='rate_type',
#                  symbol=None,
#                  hover_name='symbol',
#                  hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#                  text='symbol',
#                  line_group='rate_type',
#                  # markers=True,
#                  )

# fig = px.scatter(debt_secs,
#                  # x='price\u0394\u0025',
#                  x='price',
#                  y='shrs_outstd',
#                  # color='is_cumul',
#                  symbol=None,
#                  # size='shrs_outstd',
#                  # size='is_cumul',
#                  # hover_name='symbol',
#                  # hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#                  # text='symbol',
#                  # orientation='v',  # 'h'
#                  # trendline='rolling',  # 'ols', 'lowess', 'expanding','rolling', 'ewm'
#                  # trendline_options={'alpha': 0.4, 'adjust': True, }, 'ewm'
#                  # trendline_options={'log_x': True, 'log_y': True}, 'ols'
#                  # trendline_options={'window': 14},  # 'rolling'
#                  )

# fig = px.scatter_3d(debt_secs, x='ytm', y='ytc', z='cy', color='debt_type', size='shrs_outstd',
#                     hover_name='symbol', text='symbol', )

# traces = list(fig.select_traces())
# scenes = list(fig.select_scenes())
#
# fig.update_xaxes(zeroline=True, zerolinewidth=3, zerolinecolor='black',
#                  # tickmode='linear', tick0=0, dtick=0.25, tickfont=dict(size=10),
#                  rangemode='tozero',
#                  )
# fig.update_yaxes(zeroline=True, zerolinewidth=3, zerolinecolor='black',
#                  # tickmode='linear', tick0=0, dtick=0.5, tickfont=dict(size=10),
#                  rangemode='tozero',
#                  )
#
# fig.update_scenes(xaxis=dict(zeroline=True, zerolinewidth=5, zerolinecolor='grey', tickfont=dict(size=10),
#                              # tickmode='auto', nticks=20,
#                              tickmode='linear', tick0=0, dtick=0.2,
#                              rangemode='tozero',
#                              # tickmode='array', tickvals=[], ticktext=[],
#
#                              ),
#
#                   yaxis=dict(zeroline=True, zerolinewidth=5, zerolinecolor='grey', tickfont=dict(size=10),
#                              # tickmode='auto', nticks=20,
#                              tickmode='linear', tick0=0, dtick=0.5,
#                              rangemode='tozero',
#
#                              ),
#                   zaxis=dict(zeroline=True, zerolinewidth=5, zerolinecolor='grey', tickfont=dict(size=10),
#                              tickmode='linear', tick0=0, dtick=0.2,
#                              rangemode='tozero',
#                              )
#                   )


# fig = px.histogram(debt_secs,
#                    x=['cy', 'price\u0394\u0025'],
#                    # y='shrs_outstd',
#                    # color='debt_type',
#                    # hover_name='symbol',
#                    # hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#                    # # histnorm='percent', # 'percent', 'probability', 'density', 'probability density'
#                    # histfunc='avg',  # 'count', 'sum', 'avg', 'min', 'max'
#                    # barmode='group',  # 'group', 'overlay' or 'relative'
#                    # orientation='h',  # 'v', 'h'
#                    # nbins=0.2,
#                    )

# fig = px.ecdf(debt_secs,
#               x='ytm',
#               # x=['ytm', 'ytc'],
#               # y='price\u0394\u0025',
#               # color='rate_type',
#               # text='symbol',
#               symbol='rate_type',
#               #               hover_name='symbol',
#               #               hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#               # markers=True,
#               )

# y='price\u0394\u0025',
# fig = px.bar(debt_secs,
#              x='debt_type',
#              # y=['debt_type', 'sp_rating'],
#              y='shrs_outstd',
#              # y='cy',
#              # color='rate_type',
#              # text='symbol',
#              # hover_name='symbol',
#              # hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#              barmode='group',
#              orientation='v',
#              )


# fig = px.box(debt_secs,
#              # x='liq_price',
#              # y='shrs_outstd',
#              y=['sp_rating', 'debt_type'],
#              # y='cy',
#              color='rate_type',
#
#              hover_name='symbol',
#              hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#
#              facet_row='sp_rating',
#              facet_col=None,
#              orientation='v',
#              points='all',
#              )

# fig = px.violin(debt_secs,
#                 x=['ytm', 'ytc'],
#                 # x='shrs_outstd',
#                 # y=['sp_rating', 'debt_type'],
#                 y='shrs_outstd',
#                 # y='cy',
#                 # color='rate_type', # px.NO_COLOR
#
#                 hover_name='symbol',
#                 hover_data=['eff_cpn', 'br_prem', 'acc_div', 'duration'],
#
#                 # facet_row='sp_rating',
#                 # facet_col=None,
#                 orientation='v',
#                 points='all',
#                 box=True,
#                 )

fig = go.Figure(data=[go.Table(header=dict(values=list(debt_secs.columns),
                                           # fill_color='paleturquoise',
                                           align='center'),
                               cells=dict(values=[debt_secs[c] for c in debt_secs.columns],
                                          # fill_color='lavender',
                                          align='center'),
                               columnwidth=[120, 400],
                               ),

                      ])
fig.show()
# fig = ff.create_distplot([debt_secs['ytm'].dropna()], ['ytm'], bin_size=0.5)

# config = {'displaylogo': False,
#           'scrollZoom': True,
#           'modeBarButtonsToRemove': [],  # 'zoom', 'pan'
#           'modeBarButtonsToAdd': ['drawline',
#                                   'drawopenpath',
#                                   'drawclosedpath',
#                                   'drawcircle',
#                                   'drawrect',
#                                   'eraseshape',
#                                   ],
#
#           # 'showTips': True,
#           }
#
# fig.show(config=config)
