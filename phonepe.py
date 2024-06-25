import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json


#sql connection

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="root",
                               database = "phonepe_pulse")

mycursor = mydb.cursor()

#agg_insurance_df

mycursor.execute("SELECT * FROM phonepe_pulse.aggregated_insurance")

table1 = mycursor.fetchall()
mydb.commit()

Aggre_insurance = pd.DataFrame(table1,columns= ("States","Years","Quarter","Transaction_type","Transaction_count",
                                                "Transaction_amount"))

#agg_transaction_df

mycursor.execute("SELECT * FROM phonepe_pulse.aggregated_transaction")

table2 = mycursor.fetchall()
mydb.commit()

Aggre_transaction = pd.DataFrame(table2,columns= ("States","Years","Quarter","Transaction_type","Transaction_count",
                                                "Transaction_amount"))

#agg_user_df

mycursor.execute("SELECT * FROM phonepe_pulse.aggregated_user")

table3 = mycursor.fetchall()
mydb.commit()

Aggre_user = pd.DataFrame(table3,columns= ("States","Years","Quarter","Brands","Transaction_count",
                                                "Percentage"))


#map insurance df

mycursor.execute("SELECT * FROM phonepe_pulse.map_insurance")

table4 = mycursor.fetchall()
mydb.commit()

map_insurance = pd.DataFrame(table4,columns= ("States","Years","Quarter","Districts","Transaction_count",
                                                "Transaction_amount"))

#map transaction df

mycursor.execute("SELECT * FROM phonepe_pulse.map_transaction")

table5 = mycursor.fetchall()
mydb.commit()

map_transaction = pd.DataFrame(table5,columns= ("States","Years","Quarter","Districts","Transaction_count",
                                                "Transaction_amount"))

#map user df

mycursor.execute("SELECT * FROM phonepe_pulse.map_user")

table6 = mycursor.fetchall()
mydb.commit()

map_user = pd.DataFrame(table6,columns= ("States","Years","Quarter","Districts","RegisteredUsers",
                                                "AppOpens"))

#top insurance df

mycursor.execute("SELECT * FROM phonepe_pulse.top_insurance")

table7 = mycursor.fetchall()
mydb.commit()

top_insurance = pd.DataFrame(table7,columns= ("States","Years","Quarter","Pincodes","Transaction_count",
                                                "Transaction_amount"))


#top transaction df

mycursor.execute("SELECT * FROM phonepe_pulse.top_transaction")

table8 = mycursor.fetchall()
mydb.commit()

top_transaction = pd.DataFrame(table8,columns= ("States","Years","Quarter","Pincodes","Transaction_count",
                                                "Transaction_amount"))

#top user df

mycursor.execute("SELECT * FROM phonepe_pulse.top_user")

table9 = mycursor.fetchall()
mydb.commit()

top_user = pd.DataFrame(table9,columns= ("States","Years","Quarter","Pincodes","RegisteredUsers"))

##########################################################################################################################################

def Transaction_amount_count_Y(df,year):

    trans_amount_count = df[df["Years"] == year]
    trans_amount_count.reset_index(drop = True, inplace = True)

    trans_amount_count_group = trans_amount_count.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    trans_amount_count_group.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(trans_amount_count_group , x='States' , y = "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Agsunset_r,height= 600,width=550)
        st.plotly_chart(fig_amount)


    with col2:
        fig_count = px.bar(trans_amount_count_group , x='States' , y = "Transaction_count",title= f"{year} TRANSACTION COUNT",
                            color_discrete_sequence= px.colors.sequential.Pinkyl_r,height=600,width=550)
        st.plotly_chart(fig_count)

    
    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data_1 = json.loads(response.content)
        states_name = []
        for feature in data_1['features']:
            states_name.append(feature['properties']['ST_NM'])

        states_name.sort()

        fig_india_1 = px.choropleth( trans_amount_count_group,
                                    geojson=data_1,
                                    locations="States",
                                    featureidkey="properties.ST_NM",
                                    color="Transaction_amount",
                                    color_continuous_scale="Rainbow",
                                    range_color=( trans_amount_count_group["Transaction_amount"].min(),
                                                trans_amount_count_group["Transaction_amount"].max()),
                                    hover_name="States",
                                    title=f"{year} TRANSACTION AMOUNT",
                                    fitbounds="geojson",  # Use 'geojson' for fitting the map bounds to the GeoJSON data
                                    height=600,
                                    width=600)
        

        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth( trans_amount_count_group,
                                geojson=data_1,
                                locations="States",
                                featureidkey="properties.ST_NM",
                                color="Transaction_count",
                                color_continuous_scale="Rainbow",
                                range_color=( trans_amount_count_group["Transaction_count"].min(),
                                                trans_amount_count_group["Transaction_count"].max()),
                                hover_name="States",
                                title=f"{year} TRANSACTION COUNT",
                                fitbounds="geojson",  # Use 'geojson' for fitting the map bounds to the GeoJSON data
                                height=600,
                                width=600)


        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return trans_amount_count

def Transaction_amount_count_Y_Q(df, quarter):
    trans_amount_count = df[df["Quarter"] == quarter]
    trans_amount_count.reset_index(drop = True, inplace = True)

    trans_amount_count_group = trans_amount_count.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    trans_amount_count_group.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(trans_amount_count_group , x='States' , y = "Transaction_amount",title= f"{trans_amount_count['Years'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Agsunset_r,height = 600,width = 550)
        st.plotly_chart(fig_amount)


    with col2:
        fig_count = px.bar(trans_amount_count_group , x='States' , y = "Transaction_count",title= f"{trans_amount_count['Years'].min()} Year {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence= px.colors.sequential.Pinkyl_r,height = 600,width = 550)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data_1 = json.loads(response.content)
        states_name = []
        for feature in data_1['features']:
            states_name.append(feature['properties']['ST_NM'])

        states_name.sort()

        fig_india_1 = px.choropleth( trans_amount_count_group,
                                    geojson=data_1,
                                    locations="States",
                                    featureidkey="properties.ST_NM",
                                    color="Transaction_amount",
                                    color_continuous_scale="Rainbow",
                                    range_color=( trans_amount_count_group["Transaction_amount"].min(),
                                                trans_amount_count_group["Transaction_amount"].max()),
                                    hover_name="States",
                                    title=f"{trans_amount_count['Years'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT",
                                    fitbounds="geojson",  # Use 'geojson' for fitting the map bounds to the GeoJSON data
                                    height=600,
                                    width=600)
        

        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth( trans_amount_count_group,
                                geojson=data_1,
                                locations="States",
                                featureidkey="properties.ST_NM",
                                color="Transaction_count",
                                color_continuous_scale="Rainbow",
                                range_color=( trans_amount_count_group["Transaction_count"].min(),
                                            trans_amount_count_group["Transaction_count"].max()),
                                hover_name="States",
                                title=f"{trans_amount_count['Years'].min()} Year {quarter} QUARTER TRANSACTION COUNT",
                                fitbounds="geojson",  # Use 'geojson' for fitting the map bounds to the GeoJSON data
                                height=600,
                                width=600)


        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return trans_amount_count

    
def Aggre_transaction_type(df, state):

    trans_amount_count = df[df["States"] == state]
    trans_amount_count.reset_index(drop = True, inplace = True)

    trans_amount_count_group = trans_amount_count.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    trans_amount_count_group.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= trans_amount_count_group, names = "Transaction_type", values = "Transaction_amount",
                        width = 600 ,title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.25)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2 = px.pie(data_frame= trans_amount_count_group,names = "Transaction_type",values = "Transaction_count",
                        width = 600 ,title = f"{state.upper()} TRANSACTION COUNT", hole = 0.25)
        st.plotly_chart(fig_pie_2)

def aggre_user_plot_1(df,year):
    aggre_user_Y = df[df["Years"] == year]
    aggre_user_Y.reset_index(drop = True, inplace= True)
    aggre_user_Y_G = aggre_user_Y.groupby("Brands")[["Transaction_count"]].sum()
    aggre_user_Y_G.reset_index(inplace = True)

    fig_bar_1 = px.bar(aggre_user_Y_G, x = "Brands", y = "Transaction_count",title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.haline,hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aggre_user_Y


#agg user analysis_2
def Aggre_user_plot2(df,quarter):
    aggre_user_Y_Q = df[df["Quarter"] == quarter]
    aggre_user_Y_Q.reset_index(drop = True, inplace= True)

    aggre_user_Y_G = aggre_user_Y_Q.groupby("Brands")[["Transaction_count"]].sum()
    aggre_user_Y_G.reset_index(inplace= True)


    fig_bar_1 = px.bar(aggre_user_Y_G, x = "Brands", y = "Transaction_count",title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.haline,hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aggre_user_Y_Q

#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    aggre_user_Y_Q_S= df[df["States"] == state]
    aggre_user_Y_Q_S.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(aggre_user_Y_Q_S, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)

    st.plotly_chart(fig_line_1)


    ##############################################################################################################################

#map insurance districts
def map_insur_district(df, state):

    trans_amount_count = df[df["States"] == state]
    trans_amount_count.reset_index(drop = True, inplace = True)
    
    trans_amount_count_group= trans_amount_count.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    trans_amount_count_group.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
    
        fig_bar_1 = px.bar(trans_amount_count_group, x="Transaction_amount", y="Districts", orientation="h",height=600,
                    title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2= px.bar(trans_amount_count_group, x= "Transaction_count", y= "Districts", orientation= "h",height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

#######################################################


#map user plot 1

def map_user_plot_1(df, year):
    map_user_Y = df[df["Years"] == year]
    map_user_Y.reset_index(drop = True, inplace= True)
    map_user_Y_G = map_user_Y.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    map_user_Y_G.reset_index(inplace = True)

    fig_line_1= px.line(map_user_Y_G, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTEREDUSERS APPOPENS",width= 1000,height=800, markers= True)

    st.plotly_chart(fig_line_1)

    return map_user_Y

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#map user plot 2

def map_user_plot_2(df, quarter):
    map_user_YQ = df[df["Quarter"] == quarter]
    map_user_YQ.reset_index(drop = True, inplace= True)

    map_user_Y_G = map_user_YQ.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    map_user_Y_G.reset_index(inplace = True)

    fig_line_1= px.line(map_user_Y_G, x= "States", y= ["RegisteredUsers", "AppOpens"],
                        title= f"{df['Years'].min()} {quarter} REGISTEREDUSERS APPOPENS",width= 1000,height=800, markers= True,
                        color_discrete_sequence=px.colors.sequential.PuRd_r)

    st.plotly_chart(fig_line_1)

    return map_user_YQ
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# map user plot 3
def map_user_plot_3(df, states):
    map_user_YQS = df[df["States"] == states]
    map_user_YQS.reset_index(drop = True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_mu_bar_1 = px.bar(map_user_YQS, x= "RegisteredUsers", y= "Districts", orientation="h",
                            title= f"{states.upper()} REGISTEREDUSERS", height= 800, color_discrete_sequence=px.colors.sequential.haline)
        st.plotly_chart(fig_mu_bar_1)
    
    with col2:
        fig_mu_bar_2 = px.bar(map_user_YQS, x= "AppOpens", y= "Districts", orientation="h",
                            title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_mu_bar_2)

################################################################################################################################
def top_insurance_plot_1(df,state):
    top_insur_TACY = df[df["States"] == state]
    top_insur_TACY.reset_index(drop = True, inplace= True)

    top_insur_Y_G = top_insur_TACY.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    top_insur_Y_G.reset_index(inplace = True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_TI_bar_1 = px.bar(top_insur_TACY, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                            title= "TRANSACTION AMOUNT", height= 600, width=550, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_TI_bar_1)

    with col2:
        fig_TI_bar_2 = px.bar(top_insur_TACY, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                            title= "TRANSACTION COUNT", height= 600,  width=550, color_discrete_sequence=px.colors.sequential.haline)
        st.plotly_chart(fig_TI_bar_2)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def top_user_plot_1(df,year):
    top_user_Y = df[df["Years"] == year]
    top_user_Y.reset_index(drop = True, inplace= True)

    top_user_Y_G = top_user_Y.groupby(["States", "Quarter"])[["RegisteredUsers"]].sum()
    top_user_Y_G.reset_index(inplace = True)

    fig_tu_plot_1 = px.bar(top_user_Y_G, x= "States", y= "RegisteredUsers", color= "Quarter",hover_name="States",
                        width=1000, height= 800,title=f"{year} REGISTEREDUSERS",
                        color_discrete_sequence=px.colors.sequential.Burgyl)
    st.plotly_chart(fig_tu_plot_1)

    return top_user_Y

#top_user_plot_2
def top_user_plot_2(df, state):
    top_user_Y_S = df[df["States"] == state]
    top_user_Y_S.reset_index(drop = True, inplace= True)

    fig_tu_plot_2 = px.bar(top_user_Y_S, x= "Quarter", y= "RegisteredUsers", title="REGISTEREDUSERS PINCODES QUARTERS",
                        width= 1000, height= 800,color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_tu_plot_2)

#################################################### top_chart_transaction_amount ############################################################

def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="root",
                                database = "phonepe_pulse")

    mycursor = mydb.cursor()
    #plot 1 
    query1 = f'''select states, sum(transaction_amount) AS transaction_amount 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_amount desc
                limit 10'''
    mycursor.execute(query1)
    table = mycursor.fetchall()
    mydb.commit()

    df1 = pd.DataFrame(table,columns=("states","transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(df1 , x='states' , y = "transaction_amount",title= f"HEAD 10 OF TRANSACTION AMOUNT",hover_name= "states",
                            color_discrete_sequence= px.colors.sequential.Agsunset_r,height = 600,width = 550)
        st.plotly_chart(fig_amount)

    #plot 2
    query2 = f'''select states, sum(transaction_amount) AS transaction_amount 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_amount 
                limit 10'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df2 = pd.DataFrame(table_2,columns=("states","transaction_amount"))
    
    with col2:
        fig_amount2 = px.bar(df2 , x='states' , y = "transaction_amount",title= f"TAIL 10 OF TRANSACTION AMOUNT",hover_name= "states",
                            color_discrete_sequence= px.colors.sequential.Bluered,height = 600,width = 550)
        st.plotly_chart(fig_amount2)


    #plot 3
    query3 = f'''select states, avg(transaction_amount) AS transaction_amount 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_amount 
            '''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(table_3,columns=("states","transaction_amount"))

    fig_amount3 = px.bar(df3 , x='states' , y = "transaction_amount",title= f"AVERGE OF TRANSACTION AMOUNT",hover_name= "states",
                        color_discrete_sequence= px.colors.sequential.Bluered_r,height = 600,width = 950)
    st.plotly_chart(fig_amount3)

########################################### top_chart_transaction_count #################################################################


def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="root",
                                database = "phonepe_pulse")

    mycursor = mydb.cursor()
    #plot 1 
    query1 = f'''select states, sum(transaction_count) AS transaction_count 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_count desc
                limit 10'''
    mycursor.execute(query1)
    table = mycursor.fetchall()
    mydb.commit()

    df1 = pd.DataFrame(table,columns=("states","transaction_count"))


    col1, col2 = st.columns(2)
    with col1:
        fig_count = px.bar(df1 , x='states' , y = "transaction_count",title= f"HEAD 10 OF TRANSACTION COUNT",hover_name= "states",
                            color_discrete_sequence= px.colors.sequential.Agsunset_r,height = 600,width = 550)
        st.plotly_chart(fig_count)

    #plot 2
    query2 = f'''select states, sum(transaction_count) AS transaction_count 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_count 
                limit 10'''
    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df2 = pd.DataFrame(table_2,columns=("states","transaction_count"))

    with col2:
        fig_count2 = px.bar(df2 , x='states' , y = "transaction_count",title= f"TAIL 10 OF TRANSACTION COUNT",hover_name= "states",
                            color_discrete_sequence= px.colors.sequential.Bluered,height = 600,width = 550)
        st.plotly_chart(fig_count2)


    #plot 3
    query3 = f'''select states, avg(transaction_count) AS transaction_count 
                from phonepe_pulse.{table_name}
                group by states
                order by transaction_count 
            '''
    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(table_3,columns=("states","transaction_count"))

    fig_count3 = px.bar(df3 , x='states' , y = "transaction_count",title= f"AVERGE OF TRANSACTION COUNT",hover_name= "states",
                        color_discrete_sequence= px.colors.sequential.Bluered_r,height = 600,width = 950)
    st.plotly_chart(fig_count3)

###############################################top_chart_registered_user-states ##################################################

def top_chart_registered_user(table_name, state):
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="root",
                                database = "phonepe_pulse")
    mycursor = mydb.cursor()
    
    query1= f'''SELECT Districts, SUM(RegisteredUsers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "registereduser"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="Districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT Districts, SUM(RegisteredUsers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY registereduser
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "registereduser"))

    with col2:
        fig_amount2= px.bar(df_2, x="Districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount2)

    #plot_3
    query3= f'''SELECT Districts, AVG(RegisteredUsers) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY Districts
                ORDER BY registereduser;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "registereduser"))

    fig_amount3= px.bar(df_3, y="Districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount3)

############################################### top_chart_registered_user-Districts #############################################################

def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="root",
                                database = "phonepe_pulse")
    mycursor = mydb.cursor()
    
    query1= f'''select states, SUM(RegisteredUsers) AS registereduser
                from {table_name}
                group by states
                order by registereduser DESC
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registereduser"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, SUM(RegisteredUsers) AS registereduser
                from {table_name}
                group by states
                order by registereduser
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registereduser"))
    
    with col2:
        fig_amount2= px.bar(df_2, x="states", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount2)

    #plot_3
    query3= f'''select states, AVG(RegisteredUsers) AS registereduser
                from {table_name}
                group by states
                order by registereduser;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registereduser"))

    fig_amount3= px.bar(df_3, y="states", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount3)

################################################ top_chart_appopens ##############################################################

def top_chart_appopens(table_name, state):
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="root",
                                database = "phonepe_pulse")
    mycursor = mydb.cursor()
    
    query1= f'''select Districts, SUM(AppOpens) AS appopens
                from {table_name}
                where states= '{state}'
                group by Districts
                order by appopens DESC
                limit 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("Districts", "appopens"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="Districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select Districts, SUM(AppOpens) AS appopens
                from {table_name}
                where states= '{state}'
                group by Districts
                order by appopens
                limit 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("Districts", "appopens"))

    with col2:
        fig_amount2= px.bar(df_2, x="Districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount2)

    #plot_3
    query3= f'''select Districts, AVG(AppOpens) AS appopens
                from {table_name}
                where states= '{state}'
                group by Districts
                order by appopens;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("Districts", "appopens"))

    fig_amount3= px.bar(df_3, y="Districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount3)


 ################################################### STREAMLIT PART ###################################################################################   

#streamlit part

st.set_page_config(layout="wide")
st.title(':violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]')

with st.sidebar:
    select = option_menu("MAIN MENU",['HOME' , 'DATA EXPLORATION','TOP CHARTS'])

if select == 'HOME':
    if select == "Home":
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')

    st.write("---")
elif select == 'DATA EXPLORATION':

    tab1,tab2,tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select The Method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])

        if method == "Aggregated Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years_ai = st.slider("Select the Year", Aggre_insurance['Years'].min(), Aggre_insurance['Years'].max(), Aggre_insurance['Years'].min())

             
            trans_amount_count_Y = Transaction_amount_count_Y(Aggre_insurance, years_ai)

            col1,col2 = st.columns(2)

            with col1:
                quarter_ai = st.slider("Select the Quarter",trans_amount_count_Y['Quarter'].min(),trans_amount_count_Y['Quarter'].max(),trans_amount_count_Y['Quarter'].min())
            Transaction_amount_count_Y_Q(trans_amount_count_Y, quarter_ai)

             #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        elif method == "Aggregated Transaction":
            col1,col2 = st.columns(2)
            with col1:
                years_at = st.slider("Select the Year_AT",Aggre_transaction['Years'].min(),Aggre_transaction['Years'].max(),Aggre_transaction['Years'].min())
             
            Aggre_trans_trans_amount_count_Y = Transaction_amount_count_Y(Aggre_transaction, years_at)

            
            col1,col2 = st.columns(2)
            with col1:
                states_at = st.selectbox("Select the States_AT", Aggre_trans_trans_amount_count_Y["States"].unique())

            Aggre_transaction_type(Aggre_trans_trans_amount_count_Y, states_at)

            col1,col2 = st.columns(2)

            with col1:
                quarter_at = st.slider("Select the Quarter_AT",Aggre_trans_trans_amount_count_Y['Quarter'].min(),Aggre_trans_trans_amount_count_Y['Quarter'].max(),Aggre_trans_trans_amount_count_Y['Quarter'].min())
            Aggre_transaction_trans_amount_count_Y_Q = Transaction_amount_count_Y_Q(Aggre_trans_trans_amount_count_Y, quarter_at)

            col1,col2 = st.columns(2)
            with col1:
                states_at = st.selectbox("Select the States_AT", Aggre_transaction_trans_amount_count_Y_Q["States"].unique(), key="unique_key_here")


            Aggre_transaction_type(Aggre_transaction_trans_amount_count_Y_Q, states_at)

            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        elif method == "Aggregated User":
            col1,col2 = st.columns(2)
            with col1:
                years_au = st.slider("Select the Year_AU",Aggre_user['Years'].min(),Aggre_user['Years'].max(),Aggre_user['Years'].min())
             
            Aggre_user_Year = aggre_user_plot_1(Aggre_user,years_au)

            col1,col2 = st.columns(2)

            with col1:
                quarter_au = st.slider("Select the Quarter_AU",Aggre_user_Year['Quarter'].min(),Aggre_user_Year['Quarter'].max(),Aggre_user_Year['Quarter'].min())
            Aggre_user_Year_Quarter = Aggre_user_plot2(Aggre_user_Year, quarter_au)

            col1,col2 = st.columns(2)
            with col1:
                states_au = st.selectbox("Select the States_AU", Aggre_user_Year_Quarter["States"].unique())
            Aggre_user_Year_Quarter_States = Aggre_user_plot_3(Aggre_user_Year_Quarter, states_au)

########################################################################################################################################################


    with tab2:
        method_2 = st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":

            col1,col2 = st.columns(2)

            with col1:
                years_mi = st.slider("Select the Year_MI", map_insurance['Years'].min(), map_insurance['Years'].max(), map_insurance['Years'].min(), key="year_slider")
             
            map_insur_trans_amount_count_Y = Transaction_amount_count_Y(map_insurance, years_mi)

            col1,col2 = st.columns(2)

            with col1:

                states_mi = st.selectbox("Select the States_MI", map_insur_trans_amount_count_Y["States"].unique(), key="states_selectbox")

            map_insur_district(map_insur_trans_amount_count_Y, states_mi)

            col1,col2 = st.columns(2)
             
            with col1:
                quarter_mi = st.slider("Select the Quarter_MI", map_insur_trans_amount_count_Y['Quarter'].min(), map_insur_trans_amount_count_Y['Quarter'].max(), map_insur_trans_amount_count_Y['Quarter'].min(), key="quarter_slider")

            map_insur_trans_amount_count_Y_Q = Transaction_amount_count_Y_Q(map_insur_trans_amount_count_Y, quarter_mi)

            col1,col2 = st.columns(2)
            with col1:
               states_mi = st.selectbox("Select the States_MI", map_insur_trans_amount_count_Y_Q["States"].unique())


            map_insur_district(map_insur_trans_amount_count_Y_Q, states_mi)

            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        elif method_2 == "Map Transaction":
            col1,col2 = st.columns(2)

            with col1:
                years_mt = st.slider("Select the Year_MT", map_transaction['Years'].min(), map_transaction['Years'].max(), map_transaction['Years'].min(), key="year_slider")
             
            map_trans_trans_amount_count_Y = Transaction_amount_count_Y(map_transaction, years_mt)

            col1,col2 = st.columns(2)

            with col1:

                states_mt = st.selectbox("Select the States_MT", map_trans_trans_amount_count_Y["States"].unique(), key="states_selectbox")

            map_insur_district(map_trans_trans_amount_count_Y, states_mt)

            col1,col2 = st.columns(2)
             
            with col1:
                quarter_mt = st.slider("Select the Quarter_MT", map_trans_trans_amount_count_Y['Quarter'].min(), map_trans_trans_amount_count_Y['Quarter'].max(), map_trans_trans_amount_count_Y['Quarter'].min(), key="quarter_slider")

            map_trans_trans_amount_count_Y_Q = Transaction_amount_count_Y_Q(map_trans_trans_amount_count_Y, quarter_mt)

            col1,col2 = st.columns(2)
            with col1:
               states_mt = st.selectbox("Select the States_MT", map_trans_trans_amount_count_Y_Q["States"].unique(), key="states_mt_selectbox")

            map_insur_district(map_trans_trans_amount_count_Y_Q, states_mt)

             ## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
           
        elif method_2 == "Map User":
            
            col1,col2 = st.columns(2)

            with col1:
                years_mu = st.slider("Select the Year_MU", map_user['Years'].min(), map_user['Years'].max(), map_user['Years'].min(), key="year_slider")
             
            map_user_year = map_user_plot_1(map_user, years_mu)

            col1,col2 = st.columns(2)
             
            with col1:
                quarter_mu = st.slider("Select the Quarter_MU", map_user_year['Quarter'].min(), map_user_year['Quarter'].max(), map_user_year['Quarter'].min(), key="quarter_slider")

            map_user_Y_Q = map_user_plot_2(map_user_year, quarter_mu)

            col1,col2 = st.columns(2)
            with col1:
               states_mu = st.selectbox("Select the States_MU", map_user_Y_Q["States"].unique(), key="states_selectbox")

            map_user_plot_3(map_user_Y_Q, states_mu)

##############################################################################################################################################################

    with tab3:
        method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":
            col1,col2 = st.columns(2)

            with col1:
                years_ti = st.slider("Select the Year_TI", top_insurance['Years'].min(), top_insurance['Years'].max(), top_insurance['Years'].min(), key="year_slider_ti")

             
            top_insur_trans_amount_count_Y = Transaction_amount_count_Y(top_insurance, years_ti)

            
            col1,col2 = st.columns(2)
            with col1:
               states_ti = st.selectbox("Select the States_TI", top_insur_trans_amount_count_Y["States"].unique())

            top_insurance_plot_1(top_insur_trans_amount_count_Y, states_ti)

            col1,col2 = st.columns(2)
             
            with col1:
                quarter_ti = st.slider("Select the Quarter_TI", top_insur_trans_amount_count_Y['Quarter'].min(), top_insur_trans_amount_count_Y['Quarter'].max(), top_insur_trans_amount_count_Y['Quarter'].min())

            top_insur_trans_amount_count_Y_Q = Transaction_amount_count_Y_Q(top_insur_trans_amount_count_Y, quarter_ti)



         #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        elif method_3 == "Top Transaction":
            col1,col2 = st.columns(2)

            with col1:
                years_tt = st.slider("Select the Year_TT", top_transaction['Years'].min(), top_transaction['Years'].max(), top_transaction['Years'].min(), key="year_slider_ti")

             
            top_trans_trans_amount_count_Y = Transaction_amount_count_Y(top_transaction, years_tt)

            
            col1,col2 = st.columns(2)
            with col1:
               states_tt = st.selectbox("Select the States_TT", top_trans_trans_amount_count_Y["States"].unique())

            top_insurance_plot_1(top_trans_trans_amount_count_Y, states_tt)

            col1,col2 = st.columns(2)
             
            with col1:
                quarter_tt = st.slider("Select the Quarter_TT", top_trans_trans_amount_count_Y['Quarter'].min(), top_trans_trans_amount_count_Y['Quarter'].max(), top_trans_trans_amount_count_Y['Quarter'].min())

            top_trans_trans_amount_count_Y_Q = Transaction_amount_count_Y_Q(top_trans_trans_amount_count_Y, quarter_tt)


         #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        elif method_3 == "Top User":
            col1,col2 = st.columns(2)

            with col1:
                years_tu = st.slider("Select the Year_TU", top_user['Years'].min(), top_user['Years'].max(), top_user['Years'].min())

            top_user_year = top_user_plot_1(top_user,years_tu)

            col1,col2 = st.columns(2)
            with col1:
               states_tu = st.selectbox("Select the States_TT", top_user_year["States"].unique())

            top_user_plot_2(top_user_year, states_tu)
 #####################################################################################################################################################33
elif select == "TOP CHARTS":
    questions = [
        "1. Transaction Amount and Count of Aggregated Insurance",
        "2. Transaction Amount and Count of Map Insurance",
        "3. Transaction Amount and Count of Top Insurance",
        "4. Transaction Amount and Count of Aggregated Transaction",
        "5. Transaction Amount and Count of Map Transaction",
        "6. Transaction Amount and Count of Top Transaction",
        "7. Transaction Count of Aggregated User",
        "8. Registered users of Map User",
        "9. App opens of Map User",
        "10. Registered users of Top User"
    ]

    selected_question = st.selectbox("Select a Questions:", questions)

    if selected_question:    
        if selected_question == "1. Transaction Amount and Count of Aggregated Insurance":
            st.subheader(":violet[TRANSACTION AMOUNT OF AGGREGATED INSURANCE]")
            top_chart_transaction_amount("aggregated_insurance")

            st.subheader(":violet[TRANSACTION COUNT OF AGGREGATED INSURANCE]")
            top_chart_transaction_count("aggregated_insurance")

        elif selected_question == "2. Transaction Amount and Count of Map Insurance":
            st.subheader(":violet[TRANSACTION AMOUNT OF MAP INSURANCE]")
            top_chart_transaction_amount("map_insurance")

            st.subheader(":violet[TRANSACTION COUNT OF MAP INSURANCE]")
            top_chart_transaction_count("map_insurance")

        elif selected_question == "3. Transaction Amount and Count of Top Insurance":
            st.subheader(":violet[TRANSACTION AMOUNT OF TOP INSURANCE]")
            top_chart_transaction_amount("top_insurance")

            st.subheader(":violet[TRANSACTION COUNT OF TOP INSURANCE]")
            top_chart_transaction_count("top_insurance")

        elif selected_question == "4. Transaction Amount and Count of Aggregated Transaction":
            st.subheader(":violet[TRANSACTION AMOUNT OF AGGREGATED TRANSACTION]")
            top_chart_transaction_amount("aggregated_transaction")

            st.subheader(":violet[TRANSACTION COUNT OF AGGREGATED TRANSACTION]")
            top_chart_transaction_count("aggregated_transaction")

        elif selected_question == "5. Transaction Amount and Count of Map Transaction":
            st.subheader(":violet[TRANSACTION AMOUNT OF MAP TRANSACTION]")
            top_chart_transaction_amount("map_transaction")

            st.subheader(":violet[TRANSACTION COUNT OF MAP TRANSACTION]")
            top_chart_transaction_count("map_transaction")

        elif selected_question == "6. Transaction Amount and Count of Top Transaction":
            st.subheader(":violet[TRANSACTION AMOUNT OF TOP TRANSACTION]")
            top_chart_transaction_amount("top_transaction")

            st.subheader(":violet[TRANSACTION COUNT OF TOP TRANSACTION]")
            top_chart_transaction_count("top_transaction")

        elif selected_question == "7. Transaction Count of Aggregated User":
            st.subheader(":violet[TRANSACTION COUNT OF AGGREGATED USER]")
            top_chart_transaction_count("aggregated_user")

        elif selected_question == "8. Registered users of Map User":
            states = st.selectbox("Select the State", map_user["States"].unique())   
            top_chart_registered_user("map_user", states)

        elif selected_question == "9. App opens of Map User":
            states = st.selectbox("Select the State", map_user["States"].unique())   
            top_chart_appopens("map_user", states)

        elif selected_question == "10. Registered users of Top User":
            top_chart_registered_users("top_user")


       


    