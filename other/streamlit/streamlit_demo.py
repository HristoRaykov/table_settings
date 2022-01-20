import QuantLib as ql
from other import streamlit as st

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

from findata.commons.constants.columns.base import SYMBOL_COL
from research.container import YieldCurvesContainer

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

ql.IborCoupon.createIndexedCoupons()

val_date = ql.Date(22, 12, 2021)
ql.Settings.instance().evaluationDate = val_date

container = YieldCurvesContainer(val_date)

db_engine = container.db_engine
session = container.session
debt_sec_repo = container.debt_sec_repo
debt_secs_table = container.debt_secs_table
bond_data_creator = container.bond_data_creator
bond_factory = container.bond_factory

debt_secs = debt_secs_table.get_table()

# s = debt_secs.style.format({SHARES_OUTSTANDING_COL: '{:,.2f}'})
# s = debt_secs.style.set_precision(2).background_gradient('RdYlGn')
# st.table(s)
# st.dataframe(s)

# streamlit
# light
# dark
# blue
# fresh
# material



gb = GridOptionsBuilder.from_dataframe(debt_secs)
gb.configure_default_column(editable=False, resizable=True, sorteable=True)
gb.configure_side_bar(defaultToolPanel='columns')  # 'filters', 'columns'
dts = debt_secs.dtypes
string_cols = debt_secs.select_dtypes(include=['O']).columns.values.tolist()
int_cols = debt_secs.select_dtypes(include=[int]).columns.values.tolist()
float_cols = debt_secs.select_dtypes(include=[float]).columns.values.tolist()
date_cols = debt_secs.select_dtypes(include=['datetime64']).columns.values.tolist()

# SPEC_SYMBOL_COLS = [PRICE_COL, PRICE_CHANGE_COL, PRICE_CHANGE_PERC_COL, VOLUME_PERC_COL]
# float_cols = [c for c in float_cols if c not in SPEC_SYMBOL_COLS]

jscode = JsCode(
    """
    function(params) {
        return "$" + params.value
    }
    """
)
gb.configure_columns()
gb.configure_column(SYMBOL_COL, pinned='left')
gb.configure_columns(string_cols,
                     type=[],
                     filter=True,
                     # filter='agSetColumnFilter',
                     floatingFilter=True,
                     )
gb.configure_columns(int_cols, valueFormatter=jscode)
gb.configure_columns(float_cols,
                     type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                     filter='agNumberColumnFilter',
                     floatingFilter=True,
                     precision=2, )
gb.configure_columns(date_cols,
                     type=['dateColumn', "dateColumnFilter", "customDateTimeFormat"],
                     custom_format_string='yyyy-MM-dd',
                     filter=True,
                     floatingFilter=True,
                     pivot=True)

# gb.configure_selection('single', use_checkbox=False)
grid_options = gb.build()
grid_response = AgGrid(
    debt_secs,
    gridOptions=grid_options,
    width='100%',
    allow_unsafe_jscode=True,
    # theme='blue',
    key='main_grid',
)

s = 5
# debt_secs = debt_secs.style.background_gradient()
# equity_mapper = class_mapper(Equity)
# debt_sec_mapper = class_mapper(DebtSec)
# com_stk_mapper = class_mapper(ComStk)

# treasury_ts = container.treasury_term_structure
# sofr_ts = container.sofr_term_structure
# libor_ts = container.libor_term_structure

# treas_curves = get_curves(treasury_ts.term_structure, ql.Period(6, ql.Months))
# result = session.query(DebtSec).all()
# ds = debt_sec_repo.find_all_exchange_traded()

# debt_secs = debt_sec_repo.get_tables()

# debt_secs[['cy_nspread','nspread','dcf_nspread']]

# fig = px.scatter(debt_secs['ytc'], debt_secs['ytm'])
# fig = px.scatter(debt_secs, x='ytm', y='ytc', color='debt_type', size='shrs_outstd', hover_name='symbol')
# fig = px.scatter_3d(debt_secs, x='ytm', y='ytc', z='cy', color='debt_type', size='shrs_outstd',
#                     hover_name='symbol', text='symbol', )

# traces = list(fig.select_traces())
# scenes = list(fig.select_scenes())

# fig.update_xaxes(zeroline=True, zerolinewidth=3, zerolinecolor='black',
#                  # tickmode='linear', tick0=0, dtick=0.25, tickfont=dict(size=10),
#                  rangemode='tozero',
#                  )
# fig.update_yaxes(zeroline=True, zerolinewidth=3, zerolinecolor='black',
#                  # tickmode='linear', tick0=0, dtick=0.5, tickfont=dict(size=10),
#                  rangemode='tozero',
#                  )

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

# fig.show()


# st.plotly_chart(fig, use_container_width=True)

# debt_secs = debt_sec_repo.get_table(val_date.to_date())
# data = debt_secs[[SYMBOL_COL, COUPON_RATE_COL, SHARES_OUTSTANDING_COL, 'anon_12']]
symbol = 'AGNCN'
# debt_sec = debt_sec_repo.find(symbol)
#
# bond_data = bond_data_creator.create(val_date.to_date(), debt_sec)
#
# cfs, bond = bond_factory.get(bond_data)

# AgGrid(debt_secs, height=800)  # , fit_columns_on_grid_load=True
# chart = alt.Chart(debt_secs[['nspread', 'zspread', 'total_score']]).mark_circle().encode(x='nspread',
#                                                                                          y='zspread',
#                                                                                          size='total_score',
#                                                                                          color='total_score',
#                                                                                          )
# st.altair_chart(chart, use_container_width=True)


# debt_secs = st.multiselect(
#         "Choose countries", list(cfs[]), ["China", "United States of America"]
#     )
