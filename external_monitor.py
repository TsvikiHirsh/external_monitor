
import streamlit as st
import pandas
import os

"""
# External monitor
"""
with st.sidebar:
    def refresh():
        st.session_state.data = pandas.read_html("https://wnr-web.lanl.gov/NIST/index.html",parse_dates=True,index_col=0)[0]

    st.button("Refresh",on_click=refresh)

    plot_type = st.selectbox("plot type",["line","area","bar","scatter"],index=0)


    if "data" in st.session_state:

        x_param = st.multiselect("x param",st.session_state.data.columns,default=["run/counter"],max_selections=1)

        y_param = st.multiselect("y param",st.session_state.data.columns,default=["stats/total_counts"])

        x_param = x_param[0] if x_param else None
    
if "data" in st.session_state:
    match plot_type:
        case "line":
            st.line_chart(data=st.session_state.data,x=x_param, y=y_param, use_container_width=True)
        case "area":
            st.area_chart(data=st.session_state.data,x=x_param, y=y_param, use_container_width=True)
        case "bar":
            st.bar_chart(data=st.session_state.data,x=x_param, y=y_param, use_container_width=True)
        case "scatter":
            st.scatter_chart(data=st.session_state.data,x=x_param, y=y_param, use_container_width=True)

    st.dataframe(st.session_state.data)