import pandas as pd
import streamlit as st
import time
import plotly.express as px
import streamlit.components.v1 as components
import pygwalker as pyg


@st.cache_data
def load_data():
    df = pd.read_csv('D:\webapp\data\output\pkdata_dummy.csv')
    # df = px.data.gapminder()
    return df


# pre process data
# df = load_data()
# uploaded = st.file_uploader("Choose a File", type=["csv"])
# if uploaded != None:
#     df = pd.read_csv(uploaded)
#     with st.spinner("Writing to DF..."):
#         time.sleep(2)
#         st.write(df)

# columns = df.columns.to_list()
# columns.append(None)

# length = len(columns)


def create_radio_button(separate):
    values = df[separate].unique().tolist()

    # a radio button for figure selection
    figure_radio = st.sidebar.radio(
        label=f"Show figure by {separate}",
        options=values
    )
    return figure_radio


def line_plot(xval, yval, separate, group, hover, col, row):
    # a list of unique values from the group variable
    radio_button_value = create_radio_button(separate)

    # filter the datafram for each group value
    filter_data = df[(df[separate] == radio_button_value)]

    # create a canvas layout to drow the figures
    if (xval != None and yval != None):
        fig = px.line(filter_data,
                      x=xval,
                      y=yval,
                      color=group,
                      markers=True,
                      facet_col=col,
                      facet_row=row,
                      hover_data=hover
                      )
        # set the title and legend layout
        fig.update_layout(
            title=f"Title: {separate} ({radio_button_value})",
            paper_bgcolor="LightSteelBlue",
            legend={'bgcolor': "LightBlue",
                    'bordercolor': "Black",
                    'borderwidth': 2
                    },
            font=dict(
                size=20
            )
            # width=1024,
            # height=600,
        )
        st.plotly_chart(fig)


# pre process data
# df = load_data()
uploaded = st.file_uploader("Choose a File", type=["csv"])
if uploaded != None:
    df = pd.read_csv(uploaded)
    with st.spinner("Writing to DF..."):
        time.sleep(2)
        st.write(df)

    columns = df.columns.to_list()
    columns.append(None)

    length = len(columns)


# st.set_page_config(
#     page_title="Application",
#     layout="wide"
# )


def main():
    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Home",
            "Profile",
            "Plots",
            "Compare"
        ]
    )

    if page == "Home":
        st.header("Data Application")
        # st.balloons()
        # st.write(df)

    elif page == "Profile":
        xval = st.selectbox(
            label='X axis',
            options=columns,
            index=length-1
        )

        yval = st.selectbox(
            label='Y axis',
            options=columns,
            index=length-1
        )

        separate = st.selectbox(
            label='Separate Figure',
            options=columns,
            index=length-1
        )

        group = st.selectbox(
            label='Group By',
            options=columns,
            index=length-1
        )

        hover = st.multiselect(
            label='Hover',
            options=columns
        )

        col = st.selectbox(
            'Subplots in Columns',
            options=columns,
            index=length-1
        )

        row = st.selectbox(
            label='Subplots in Rows',
            options=columns,
            index=length-1
        )

        kwargs = {
            'xval': xval,
            'yval': yval,
            'separate': separate,
            'group': group,
            'hover': hover,
            'col': col,
            'row': row
        }
        if xval != None and yval != None and separate != None:
            line_plot(**kwargs)
    elif page == "Plots":
        st.title("Use Pygwalker In Streamlit")

        pyg_html = pyg.walk(df, return_html=True, dark="dark")
        components.html(pyg_html, height=700, scrolling=True)
    elif page == "Compare":
        pass

if __name__ == "__main__":
    main()
