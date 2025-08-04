import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import requests
import json
from PIL import Image
import plotly.graph_objects as go

# Set Streamlit page layout (only ONCE and at the TOP)
st.set_page_config(layout="wide")


st.markdown(
    """
    <style>
    .stApp {
        background-color: #5f259f;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("PHONEPAY DATA VISUALIZATION AND EXPLORATION")

# Database config (PostgreSQL)
engine = create_engine("postgresql+psycopg2://postgres:nivetha15@localhost:5432/phonepay_db")

# Load data from database
agg_ins_df = pd.read_sql("SELECT * FROM aggregated_insurance", con=engine)
agg_tran_df = pd.read_sql("SELECT * FROM aggregated_transaction", con=engine)
agg_user_df = pd.read_sql("SELECT * FROM aggregated_user", con=engine)

map_ins_df = pd.read_sql("SELECT * FROM map_insurance", con=engine)
map_tran_df = pd.read_sql("SELECT * FROM map_transaction", con=engine)
map_user_df = pd.read_sql("SELECT * FROM map_user", con=engine)

top_ins_df = pd.read_sql("SELECT * FROM top_insurance", con=engine)
top_tran_df = pd.read_sql("SELECT * FROM top_transaction", con=engine)
top_user_df = pd.read_sql("SELECT * FROM top_user", con=engine)

agg_ins_df["Year"] = agg_ins_df["Year"].astype(int)
agg_tran_df["Year"] = agg_tran_df["Year"].astype(int)
agg_user_df["Year"] = agg_user_df["Year"].astype(int)

map_ins_df["Year"] = map_ins_df["Year"].astype(int)
map_tran_df["Year"] = map_tran_df["Year"].astype(int)
map_user_df["Year"] = map_user_df["Year"].astype(int)

top_ins_df["Year"] = top_ins_df["Year"].astype(int)
top_tran_df["Year"] = top_tran_df["Year"].astype(int)
top_user_df["Year"] = top_user_df["Year"].astype(int)




# Plotting function
def transaction_amount_count_Y(df, Years):

    tacy = df[df["Year"] == Years]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("State")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount_1=px.bar(tacyg, x="State", y="transaction_amount", title=f"{Years} TRANSACTION_AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width = 600)
        st.plotly_chart(fig_amount_1)

    with col2:
        fig_count_1=px.bar(tacyg, x="State", y="transaction_count", title=f"{Years} TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.algae_r, height=650, width = 600)
        st.plotly_chart(fig_count_1)

    col1,col2 = st.columns(2)
    with col1:

        map_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(map_url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey = "properties.ST_NM",
                                    color = "transaction_amount",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),
                                    hover_name= "State",title= f"{Years} TRANSACTION AMOUNT",fitbounds="locations",
                                    height = 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey = "properties.ST_NM",
                                    color = "transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),
                                    hover_name= "State",title= f"{Years} TRANSACTION COUNT",fitbounds="locations",
                                    height = 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

        return tacy


def transaction_amount_count_Y_Q(df, quarter):

    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("State")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount_2=px.bar(tacyg, x="State", y="transaction_amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 650, width= 600)
        st.plotly_chart(fig_amount_2)

    with col2:

        fig_count_2=px.bar(tacyg, x="State", y="transaction_count", title=f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.algae_r, height = 650, width= 600)
        st.plotly_chart(fig_count_2)

    col1,col2 = st.columns(2)
    with col1:

        map_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(map_url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey = "properties.ST_NM",
                                    color = "transaction_amount",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),
                                    hover_name= "State",title= f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                    height = 600, width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey = "properties.ST_NM",
                                    color = "transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),
                                    hover_name= "State",title= f"{tacy['Year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                    height = 600, width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def agg_tran_transaction_type(df, state):

    tacy = df[df["State"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fie_pie_1= px.pie(data_frame= tacyg, names= "transaction_type", values="transaction_amount",
                        width=600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fie_pie_1)

    with col2:
        fie_pie_2= px.pie(data_frame= tacyg, names= "transaction_type", values="transaction_count",
                        width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fie_pie_2)

#aggregated user analysis 1
def agg_user_plot_1(df, Years):
    aguy = df[df["Year"]== Years]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["transaction_count"].sum())
    aguyg.reset_index(inplace = True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "transaction_count", title= f"{Years} BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

#aggregated user analysis 2
def agg_user_plot_2(df, quarter):
    aguyg = df[df["Quarter"]== quarter]
    aguyg.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyg.groupby("Brands")["transaction_count"].sum())
    aguyqg.reset_index(inplace = True)

    fig_bar_2= px.bar(aguyqg, x= "Brands", y= "transaction_count", title= f"{quarter} Quarter, BRANDS AND TRANSACTION COUNT",
                        width= 800, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_2)

    return aguyg


#aggregated user analysis 3
def agg_user_plot_3(df, state):
    auyqs= df[df["State"]== state]
    auyqs.reset_index(drop= True, inplace= True)
    
    fig_line_1= px.line(auyqs, x= "Brands", y= "transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS AND TRANSACTION COUNT, PERCENTAGE",
                        width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#Map Insurance
def map_ins_Districts(df, state):

    tacy = df[df["State"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("Districts")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fie_bar_2= px.bar(tacyg, x= "transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fie_bar_2)

    with col2:

        fie_bar_3= px.bar(tacyg, x= "transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fie_bar_3)

# Map User
def map_user_plot_1(df, Years):
    muy = df[df["Year"]== Years]
    muy.reset_index(drop= True, inplace= True)

    muyg=muy.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_2= px.line(muyg, x= "State", y= ["RegisteredUser", "AppOpens"],
                        title= f"{Years} REGISTEREDUSER USER, APPOPENS",
                        width= 1000, height=800, markers= True)
    st.plotly_chart(fig_line_2)

    return muy


#Map User plot_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_3= px.line(muyqg, x= "State", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Year']} YEAR {quarter} QUARTER REGISTEREDUSER, APPOPENS",
                        width= 1000, height=800, markers= True, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_3)

    return muyq


#Map User plot_3
def map_user_plot_3(df, states):
    muyqs = df[df["State"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "Districts", orientation= "h",
                        title= "REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                        title= "APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_2)

#Top Insurance plot 1
def top_ins_plot_1(df, states):
    tiy = df[df["State"]== states]
    tiy.reset_index(drop= True, inplace= True)

    fig_top_user_bar_1= px.bar(tiy, x= "Quarter", y= "transaction_amount", hover_data= "Pincodes",
                            title= "TRANSACTION AMOUNT", height=0, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_top_user_bar_1)

    fig_top_user_bar_2= px.bar(tiy, x= "Quarter", y= "transaction_count", hover_data= "Pincodes",
                            title= "TRANSACTION COUNT", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_top_user_bar_2)


def top_user_plot_1(df, Years):
    tuy=df[df["Year"]== Years]
    tuy.reset_index(drop= True, inplace= True)
    tuyg= pd.DataFrame(tuy.groupby(["State", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x ="State", y = "RegisteredUsers", color="Quarter", width=1000, height=800,
                            color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "State",
                            title= f"{Years} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["State"]== state]
    tuys.reset_index(drop= True, inplace= True)
    fig_top_plot_2= px.bar(tuys, x ="Quarter", y = "RegisteredUsers", title= "REGISTEREDUSER, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes", 
                        color_continuous_scale= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_plot_2)


def top_chart_transaction_amount(table_name):
    #Plotl_1
    query1= f'''SELECT "State", SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_amount" DESC
                Limit 10;'''


    df_1 = pd.read_sql_query(query1, engine)

    fig_amount_1= px.bar(df_1, x ="State", y = "transaction_amount", width=1000, height=800, title= "TOP 10 OF TRANSACTION AMOUNT",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "State",
                                )
    st.plotly_chart(fig_amount_1)

    #Plotl_2
    query2= f'''SELECT "State", SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_amount"; '''


    df_2 = pd.read_sql_query(query2, engine)

    fig_amount_2= px.bar(df_2, x ="State", y = "transaction_amount", width=1000, height=800, title= "LAST 10 OF TRANSACTION AMOUNT",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "State",
                                )
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT "State", AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_amount"; '''


    df_3 = pd.read_sql_query(query3, engine)

    fig_amount_3= px.bar(df_3, y ="State", x = "transaction_amount", width=1000, height=800, title= "AVERAGE OF TRANSACTION AMOUNT", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= "State",)
    st.plotly_chart(fig_amount_3)


def top_chart_transaction_count(table_name):
    #Plotl_1
    query1= f'''SELECT "State", SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_count" DESC
                Limit 10;'''


    df_1 = pd.read_sql_query(query1, engine)

    fig_amount_1= px.bar(df_1, x ="State", y = "transaction_count", width=1000, height=800, title= "TOP 10 OF TRANSACTION COUNT",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "State",
                                )
    st.plotly_chart(fig_amount_1)

    #Plotl_2
    query2= f'''SELECT "State", SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_count"; '''


    df_2 = pd.read_sql_query(query2, engine)

    fig_amount_2= px.bar(df_2, x ="State", y = "transaction_count", width=1000, height=800, title= "LAST 10 OF TRANSACTION COUNT",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "State",
                                )
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT "State", AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY "State"
                ORDER BY "transaction_count"; '''


    df_3 = pd.read_sql_query(query3, engine)

    fig_amount_3= px.bar(df_3, y ="State", x = "transaction_count", width=1000, height=800, title= "AVERAGE OF TRANSACTION COUNT", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= "State",)
    st.plotly_chart(fig_amount_3)


def top_chart_Registered_User(table_name,States):
    #Plotl_1
    query1= f'''SELECT "Districts", SUM("RegisteredUser") AS registereduser
                FROM {table_name}
                WHERE "State" = '{States}'
                GROUP BY "Districts"
                ORDER BY "registereduser" DESC
                Limit 10;'''


    df_1 = pd.read_sql_query(query1, engine)

    fig_amount_1= px.bar(df_1, x ="Districts", y = "registereduser", width=1000, height=800, title= "TOP 10 OF REGISTERED USER",
                                color_discrete_sequence= px.colors.sequential.PuBu_r,
                                )
    st.plotly_chart(fig_amount_1)
    
    #Plotl_2
    query2= f'''SELECT "Districts", SUM("RegisteredUser") AS registereduser
                FROM {table_name}
                WHERE "State" = '{States}'
                GROUP BY "Districts"
                ORDER BY "registereduser" 
                Limit 10;'''


    df_2 = pd.read_sql_query(query2, engine)

    fig_amount_2= px.bar(df_2, x ="Districts", y = "registereduser", width=1000, height=800, title= "LAST 10 OF REGISTERED USER",
                                color_discrete_sequence= px.colors.sequential.PuBu_r,
                                )
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT "Districts", AVG("RegisteredUser") AS registereduser
                FROM {table_name}
                WHERE "State" = '{States}'
                GROUP BY "Districts"
                ORDER BY "registereduser";'''


    df_3 = pd.read_sql_query(query3, engine)

    fig_amount_3= px.bar(df_3, y ="Districts", x = "registereduser", width=1000, height=800, title= "AVERAGE OF REGISTERED USER", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Magenta_r,)
    st.plotly_chart(fig_amount_3)

def top_chart_Appopens(table_name,State):
    #Plotl_1
    query1= f'''SELECT "Districts", SUM("AppOpens") AS appopens
                FROM {table_name}
                WHERE "State" = '{State}'
                GROUP BY "Districts"
                ORDER BY "appopens" DESC
                Limit 10;'''


    df_1 = pd.read_sql_query(query1, engine)

    fig_amount_1= px.bar(df_1, x ="Districts", y = "appopens", width=1000, height=800, title= "TOP 10 OF APPOPENS",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "Districts",
                                )
    st.plotly_chart(fig_amount_1)
    
    #Plotl_2
    query2= f'''SELECT "Districts", SUM("AppOpens") AS appopens
                FROM {table_name}
                WHERE "State" = '{State}'
                GROUP BY "Districts"
                ORDER BY "appopens" 
                Limit 10;'''


    df_2 = pd.read_sql_query(query2, engine)

    fig_amount_2= px.bar(df_2, x ="Districts", y = "appopens", width=1000, height=800, title= "LAST 10 OF APPOPENS",
                                color_discrete_sequence= px.colors.sequential.PuBu_r, hover_name= "Districts",
                                )
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT "Districts", AVG("AppOpens") AS appopens
                FROM {table_name}
                WHERE "State" = '{State}'
                GROUP BY "Districts"
                ORDER BY "appopens";'''


    df_3 = pd.read_sql_query(query3, engine)

    fig_amount_3= px.bar(df_3, y ="Districts", x = "appopens", width=1000, height=800, title= "AVERAGE OF APPOPENS", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= "Districts",)
    st.plotly_chart(fig_amount_3)


def top_chart_REGISTERED_USER(table_name):
    #Plotl_1
    query1= f'''SELECT "State", SUM("RegisteredUsers") AS registereduser
                FROM top_user
                GROUP BY "State"
                ORDER BY "registereduser" DESC
                Limit 10;'''


    df_1 = pd.read_sql_query(query1, engine)

    fig_amount_1= px.bar(df_1, x ="State", y = "registereduser", width=1000, height=800, title= "TOP 10 OF REGISTERED_USER",
                                color_discrete_sequence= px.colors.sequential.PuBu_r,
                                )
    st.plotly_chart(fig_amount_1)
    
    #Plotl_2
    query2= f'''SELECT "State", SUM("RegisteredUsers") AS registereduser
                        FROM top_user
                        GROUP BY "State"
                        ORDER BY "registereduser" 
                        Limit 10;'''


    df_2 = pd.read_sql_query(query2, engine)

    fig_amount_2= px.bar(df_2, x ="State", y = "registereduser", width=1000, height=800, title= "LAST 10 OF REGISTERED_USER",
                                color_discrete_sequence= px.colors.sequential.PuBu_r,
                                )
    st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT "State", AVG("RegisteredUsers") AS registereduser
                        FROM top_user
                        GROUP BY "State"
                        ORDER BY "registereduser";'''


    df_3 = pd.read_sql_query(query3, engine)

    fig_amount_3= px.bar(df_3, y ="State", x = "registereduser", width=1000, height=800, title= "AVERAGE OF REGISTERED_USER", orientation= "h",
                        color_discrete_sequence= px.colors.sequential.Magenta_r,)
    st.plotly_chart(fig_amount_3)


def question1():
    brand= agg_user_df[["Brands","transaction_count"]]
    brand1= brand.groupby("Brands")["transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                        title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def question2():
    lowest= agg_tran_df[["State", "transaction_amount"]]
    lowest1= lowest.groupby("State")["transaction_amount"].sum().sort_values(ascending= True)
    lowest2= pd.DataFrame(lowest1).reset_index().head(10)

    fig_lts= px.bar(lowest2, x= "State", y= "transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def question3():
    htd= map_tran_df[["Districts", "transaction_amount"]]
    htd1= htd.groupby("Districts")["transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def question4():
    htd= map_tran_df[["Districts", "transaction_amount"]]
    htd1= htd.groupby("Districts")["transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def question5():
    sa= map_user_df[["State", "AppOpens"]]
    sa1= sa.groupby("State")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "State", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)


    

# Sidebar navigation
with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

# Main Content
if select == "HOME":
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📲 Mobile Recharge")
        st.write("Recharge prepaid or pay postpaid bills.")
        st.button("Go")

    with col2:
        st.subheader("💸 Money Transfer")
        st.write("Send or receive money instantly.")
        st.button("Transfer")

    with col3:
        st.subheader("💡 Bill Payments")
        st.write("Electricity, DTH, Gas, Broadband & more.")
        st.button("Pay Bills")

    st.markdown("---")

# Additional Services Section
    st.subheader("Other Services")
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("🔒 **Insurance**")
        st.markdown("📈 **Investments**")
        st.markdown("🎁 **Rewards & Offers**")

    with col5:
        st.markdown("🏦 **Bank Balance Check**")
        st.markdown("💳 **Credit Cards**")
        st.markdown("🛍️ **Shopping & Gift Cards**")

        st.markdown("---")

elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])  # Keep this if you plan to add more tabs
    with tab1:
        method = st.radio("Select the method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year", int(agg_ins_df["Year"].min()),int(agg_ins_df["Year"].max()),int(agg_ins_df["Year"].min()))
            tac_Y = transaction_amount_count_Y(agg_ins_df, years)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter", int(tac_Y["Quarter"].min()),int(tac_Y["Quarter"].max()),int(tac_Y["Quarter"].min()))
            transaction_amount_count_Y_Q(tac_Y, quarter)

        elif method == "Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the years", int(agg_tran_df["Year"].min()),int(agg_tran_df["Year"].max()),int(agg_tran_df["Year"].min()))
            agg_tran_tac_Y = transaction_amount_count_Y(agg_tran_df, years)

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ty", agg_tran_tac_Y["State"].unique())
            agg_tran_transaction_type(agg_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter", int(agg_tran_tac_Y["Quarter"].min()),int(agg_tran_tac_Y["Quarter"].max()),int(agg_tran_tac_Y["Quarter"].min()))
            agg_tran_tac_Y_Q= transaction_amount_count_Y_Q(agg_tran_tac_Y, quarter)

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_typ", agg_tran_tac_Y_Q["State"].unique())
            agg_tran_transaction_type(agg_tran_tac_Y_Q, states)

        elif method == "User Analysis":
            
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year", int(agg_user_df["Year"].min()),int(agg_user_df["Year"].max()),int(agg_user_df["Year"].min()))
            agg_user_Y = agg_user_plot_1(agg_user_df, years)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter", int(agg_user_Y["Quarter"].min()),int(agg_user_Y["Quarter"].max()),int(agg_user_Y["Quarter"].min()))
            agg_user_Y_Q= agg_user_plot_2(agg_user_Y, quarter)

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State", agg_user_Y_Q["State"].unique())
            agg_user_plot_3(agg_user_Y_Q, states)


    with tab2:
        method_2 = st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":

            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year_mi", int(map_ins_df["Year"].min()),int(map_ins_df["Year"].max()),int(map_ins_df["Year"].min()))
            map_ins_tac_Y = transaction_amount_count_Y(map_ins_df, years)
            

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_ins_tac_Y["State"].unique())
            map_ins_Districts(map_ins_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter_mi", int(map_ins_tac_Y["Quarter"].min()),int(map_ins_tac_Y["Quarter"].max()),int(map_ins_tac_Y["Quarter"].min()))
            map_ins_tac_Y_Q= transaction_amount_count_Y_Q(map_ins_tac_Y, quarter)

            
            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_type", map_ins_tac_Y_Q["State"].unique())
            map_ins_Districts(map_ins_tac_Y_Q, states)

        elif method_2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year", int(map_tran_df["Year"].min()),int(map_tran_df["Year"].max()),int(map_tran_df["Year"].min()))
            map_tran_tac_Y = transaction_amount_count_Y(map_tran_df, years)
            

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_tran_tac_Y["State"].unique())
            map_ins_Districts(map_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter_mt", int(map_tran_tac_Y["Quarter"].min()),int(map_tran_tac_Y["Quarter"].max()),int(map_tran_tac_Y["Quarter"].min()))
            map_tran_tac_Y_Q= transaction_amount_count_Y_Q(map_tran_tac_Y, quarter)

            
            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_type", map_tran_tac_Y_Q["State"].unique())
            map_ins_Districts(map_tran_tac_Y_Q, states)
        

        elif method_2 == "Map User":
            
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year_mu", int(map_user_df["Year"].min()),int(map_user_df["Year"].max()),int(map_user_df["Year"].min()))
            map_user_Y = map_user_plot_1(map_user_df, years)

            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter_mu", int(map_user_Y["Quarter"].min()),int(map_user_Y["Quarter"].max()),int(map_user_Y["Quarter"].min()))
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarter)

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", map_user_Y_Q["State"].unique())
            map_user_plot_3(map_user_Y_Q, states)

            
            

    with tab3:
        method_3 = st.radio("Select The Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year_ti", int(top_ins_df["Year"].min()),int(top_ins_df["Year"].max()),int(top_ins_df["Year"].min()))
            top_ins_tac_Y = transaction_amount_count_Y(top_ins_df, years)
            

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", top_ins_tac_Y["State"].unique())
            top_ins_plot_1(top_ins_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter_mu", int(top_ins_tac_Y["Quarter"].min()),int(top_ins_tac_Y["Quarter"].max()),int(top_ins_tac_Y["Quarter"].min()))
            top_ins_tac_Y_Q= transaction_amount_count_Y_Q(top_ins_tac_Y, quarter)



        elif method_3 == "Top Transaction":


            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year_tt", int(top_tran_df["Year"].min()),int(top_tran_df["Year"].max()),int(top_tran_df["Year"].min()))
            top_tran_tac_Y = transaction_amount_count_Y(top_tran_df, years)
            

            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["State"].unique())
            top_ins_plot_1(top_tran_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarter = st.slider("Select the quarter_tu", int(top_tran_tac_Y["Quarter"].min()),int(top_tran_tac_Y["Quarter"].max()),int(top_tran_tac_Y["Quarter"].min()))
            top_tran_tac_Y_Q= transaction_amount_count_Y_Q(top_tran_tac_Y, quarter)



        elif method_3 == "Top User":
            

            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the year_tu", int(top_user_df["Year"].min()),int(top_user_df["Year"].max()),int(top_user_df["Year"].min()))
            top_user_tac_Y = top_user_plot_1(top_user_df, years)


            col1,col2 = st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_tac_Y["State"].unique())
            top_user_plot_2(top_user_tac_Y, states)

            

elif select == "TOP CHARTS":
    

    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                           "2. Transaction Amount and Count of Map insurance",
                           "3. Transaction Amount and Count of Top Insurance",
                           "4. Transaction Amount and Count of Aggregated Transaction",
                           "5. Transaction Amount and Count of Map Transaction",
                           "6. Transaction Amount and Count of Top Transaction",
                           "7. Transaction Count of Aggregated User",
                           "8. Registered user of map User",
                           "9. App opens of Map User",
                           "10. Registered users of top User",
                           "11. Top Brands Of Mobiles Used",
                           "12. States With Lowest Trasaction Amount",
                           "13. Districts With Highest Transaction Amount",
                           "14. Top 10 Districts With Lowest Transaction Amount",
                           "15. Least 10 States With AppOpens",
                           ])
    if question== "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question== "2. Transaction Amount and Count of Map insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question== "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question== "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question== "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question== "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question== "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question== "8. Registered user of map User":

        States = st.selectbox("Select the state", map_user_df["State"].unique())
        st.subheader("REGISTERED USER")
        top_chart_Registered_User("map_user",States)

    elif question== "9. App opens of Map User":

        States = st.selectbox("Select the state", map_user_df["State"].unique())
        st.subheader("APPOPENS")
        top_chart_Appopens("map_user",States)

    elif question== "10. Registered users of top User":

        States = st.selectbox("Select the state", map_user_df["State"].unique())
        st.subheader("APPOPENS")
        top_chart_REGISTERED_USER("table_name")    

    elif question=="11. Top Brands Of Mobiles Used":
        question1()

    elif question=="12. States With Lowest Trasaction Amount":
        question2()

    elif question=="13. Districts With Highest Transaction Amount":
        question3()

    elif question=="14. Top 10 Districts With Lowest Transaction Amount":
        question4()

    elif question=="15. Least 10 States With AppOpens":
        question5()
   
    

    