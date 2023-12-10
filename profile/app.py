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


def create_statistics(var, var_value, stat_by, args):
    data_filter = df[df[var] == var_value]
    print(args)
    stat = pd.DataFrame(data_filter.agg(
        **args)).reset_index().rename(columns={'index': 'stat', stat_by: var_value})
    return stat

uploaded = st.file_uploader("Choose a File", type=["csv"])
if uploaded != None:
    df = pd.read_csv(uploaded)
    st.write(df)
    columns = df.columns.to_list()
    columns.append(None)

    length = len(columns)

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
        st.header("NONMEM Patient Profile Data Application (pk/pd)")
        # st.balloons()
        # st.write(df)

    elif uploaded == None:
        st.write("Please upload a dataset")

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
        st.title("Plotting Interface")

        pyg_html = pyg.walk(df, return_html=True, dark="dark")
        components.html(pyg_html, height=700, scrolling=True)

    elif page == "Compare":
        variable = st.selectbox(
            label='Variable',
            options=columns,
            index=length-1
        )

        stat_by = st.selectbox(
            label='Statistics By',
            options=columns,
            index=length-1
        )

        stat_func = st.multiselect(
            label='Statistics',
            options=['count', 'mean', 'std', 'min', 'max', None]
        )

        stat_label = st.text_input(
            label='Statistics Label'
        )

        # create input parameters for aggregation
        if stat_label != '':
            label_list = stat_label.replace(' ', '').split(',')
            stat = list(zip(label_list, stat_func))
            print(stat)
        else:
            stat = list(zip(stat_func, stat_func))
            print("stat",stat)

        args = {}
        if stat != [(None, None)]:
            for i, j in stat:
                args[f"{i}"] = (stat_by, j)

            # unique values in variable
            values = df[variable].unique().tolist()

            prev_data = pd.DataFrame()
            for value in values:
                stat_data = create_statistics(
                    var='study',
                    var_value=value,
                    stat_by='age',
                    args=args
                )
                if prev_data.empty:
                    prev_data = pd.concat([prev_data, stat_data])
                else:
                    prev_data = pd.merge(prev_data, stat_data, on='stat')
            st.write(prev_data)


if __name__ == "__main__":
    main()
