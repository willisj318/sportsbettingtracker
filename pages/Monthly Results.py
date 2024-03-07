#from turtle import onclick
import streamlit as st
import pandas as pd
import statistics
from datetime import datetime

#import streamlit.components.v1 as components
st.set_page_config(
    page_title="Picks Grid",
    layout="wide"
    )
# Initialize connection.
# Uses st.experimental_singleton to only run once.

df=pd.read_csv("./app/data/SB.csv")

df['BET_DATE'] = pd.to_datetime(df['BET_DATE'])
vegasdf = df[(df.BET_SOURCE == 'Vegas')]
acheungerdf = df[(df.BET_SOURCE == 'Acheunger')]
myselfdf = df[(df.BET_SOURCE == 'Myself')]
dailyprofitdf = df[['BET_DATE', 'BET_NET_PROFIT']]

df2 = df

# if 'df' not in st.session_state:
#    st.session_state.df = df

st.title('Sports Bets Catalogue')

# Date Ranges, I can probably do this more efficiently somehow

jan_start_date = '2024-01-01'
jan_end_date = '2024-01-31'
feb_start_date = '2024-02-01'
feb_end_date = '2024-02-29'
mar_start_date = '2024-03-01'
mar_end_date = '2024-03-31'

def df_monthly(start_date, end_date): 
    monthly_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    return(monthly_df)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


def header_bg(BET_RESULT):
    if BET_RESULT == "Win":
        return "winbackground"
    elif BET_RESULT == "Loss":
        return "lossbackground"
    else:
        return "mvbackground"

def numberBets(start_date, end_date):
    num_bets = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    return(len(num_bets))

def totalAmountBet(start_date, end_date):
    total_bet_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    total_bet = sum(total_bet_df.BET_AMOUNT)
    return(format(float(total_bet), '.2f'))

def totalAmountWon(start_date, end_date):
    total_won_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    total_won = sum(total_won_df.BET_GROSS_PROFIT)
    return(format(float(total_won), '.2f'))

def avgOdds(start_date, end_date):
    avg_odds_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    avg_odds = statistics.mean(avg_odds_df.BET_DECIMAL_ODDS)
    return(format(float(avg_odds), '.2F'))

def winningPercentage():
    return

def roi():
    #net profit / totalbets
    return()

def totalProfit(start_date, end_date):
    total_profit_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    total_profit = sum(total_profit_df.BET_NET_PROFIT)
    return(format(float(total_profit), '.2f'))

def total_trail_vegas():
    vegas_total_profit = sum(vegasdf.BET_NET_PROFIT)
    return(format(float(vegas_total_profit), '.2f'))

def total_trail_ace():
    acheunger_profit = sum(acheungerdf.BET_NET_PROFIT)
    return(format(float(acheunger_profit), '.2f'))

def total_myself():
    myself_profit = sum(myselfdf.BET_NET_PROFIT)
    return(format(float(myself_profit), '.2f'))

remote_css(
    "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")


local_css("style.css")
cb_view_details = st.sidebar.checkbox('View Details')

if cb_view_details:
    view_details=""
else:
    view_details="""style="display: none;" """

selectbox_orderby = st.sidebar.selectbox("Order By", ('A → Z', 'Z → A', 'Bet Date ↓', 'Bet Date ↑', 'Bet Won ↓', 'Bet Lost ↑'))
#button_clicked = st.button("OK")

all_option = pd.Series(['All'], index=[9999999])

if 'selectbox_database_key' not in st.session_state:
    st.session_state.selectbox_database_key = 10
    st.session_state.selectbox_home_key = 11
    st.session_state.selectbox_bet_type_key = 20
    st.session_state.selectbox_sb_key = 30
    st.session_state.selectbox_bet_sport_key = 40
    st.session_state.selectbox_bet_date_key = 50
    st.session_state.selectbox_bet_source_key = 60

#st.write(st.session_state)

# Table Catalog/Database
    
#fv_database = df['BET_ID']
#fv_database = pd.concat([fv_database,all_option])

# Bet Sportsbook
fv_owner = df['SB_USED'].drop_duplicates()
fv_owner = pd.concat([fv_owner,all_option])
selectbox_owner = st.sidebar.selectbox(
    "Sportsbook", fv_owner, len(fv_owner)-1, key=st.session_state.selectbox_sb_key)

if selectbox_owner != 'All':
    df = df.loc[df['SB_USED'] == selectbox_owner]
else:
    df = df.loc[df['SB_USED'].isin(fv_owner)]

# Bet Source
fv_bet_source = df['BET_SOURCE'].drop_duplicates()
fv_bet_source = pd.concat([fv_bet_source,all_option])

selectbox_owner = st.sidebar.selectbox(
    "BET_SOURCE", fv_bet_source, len(fv_bet_source)-1, key=st.session_state.selectbox_bet_source_key)

if selectbox_owner != 'All':
    df = df.loc[df['BET_SOURCE'] == selectbox_owner]
else:
    df = df.loc[df['BET_SOURCE'].isin(fv_bet_source)]

# Bet Type
fv_bet_type = df['BET_TYPE'].drop_duplicates()
selectbox_bet_sport = st.sidebar.multiselect(
    'Bet Type', fv_bet_type, fv_bet_type, key=st.session_state.selectbox_bet_type_key)

if len(selectbox_bet_sport) > 0:
    df = df.loc[df['BET_TYPE'].isin(selectbox_bet_sport)]
else:
    df = df.loc[df['BET_TYPE'].isin(fv_bet_type)]

# Bet Sport
fv_bet_sport = df['BET_SPORT'].drop_duplicates()
selectbox_bet_sport = st.sidebar.multiselect(
    'Sport', fv_bet_sport, fv_bet_sport, key=st.session_state.selectbox_bet_sport_key)

if len(selectbox_bet_sport) > 0:
    df = df.loc[df['BET_SPORT'].isin(selectbox_bet_sport)]
else:
    df = df.loc[df['BET_SPORT'].isin(fv_bet_sport)]

# Filter Session Reset
def reset_button():
    st.session_state.selectbox_bet_type_key = st.session_state.selectbox_bet_type_key+1
    st.session_state.selectbox_bet_source_key = st.session_state.selectbox_bet_source_key+1
    st.session_state.selectbox_bet_sport_key = st.session_state.selectbox_bet_sport_key+1
    st.session_state.selectbox_bet_date_key = st.session_state.selectbox_bet_date_key+1
    st.session_state.selectbox_sb_key = st.session_state.selectbox_sb_key+1
    st.session_state.selectbox_home_key = st.session_state.selectbox_home_key+1


clear_button = st.sidebar.button(
    label='Clear Selections', on_click=reset_button)

if clear_button:
    df = df2

# Card order
orderby_column = ''
orderby_asc = True

if selectbox_orderby == 'A → Z':
    orderby_column = 'BET_ID'
    orderby_asc = True
elif selectbox_orderby == 'Z → A':
    orderby_column = 'BET_ID'
    orderby_asc = False
elif selectbox_orderby == 'Bet Date ↓':
    orderby_column = 'BET_DATE'
    orderby_asc = True
elif selectbox_orderby == 'Bet Date ↑':
    orderby_column = 'BET_DATE'
    orderby_asc = False
elif selectbox_orderby == 'Bet Won ↓':
    orderby_column = 'BET_RESULT'
    orderby_asc = False
elif selectbox_orderby == 'Bet Lost ↑':
    orderby_column = 'BET_RESULT'
    orderby_asc = True

tab_jan24, tab_feb24, tab_march24 = st.tabs(["January 24", "February 24", "March 24"])

df.sort_values(by=[orderby_column], inplace=True, ascending=orderby_asc)

profit_by_day = df.groupby(df.BET_DATE)['BET_NET_PROFIT'].sum()

def dailyProfit(start_date, end_date):
    total_profit_df = df[(df.BET_DATE >= start_date) & (df.BET_DATE <= end_date)]
    total_profit = total_profit_df.groupby(total_profit_df.BET_DATE)['BET_NET_PROFIT'].sum() 
    return(total_profit)

with tab_jan24:
    st.bar_chart(dailyProfit(jan_start_date, jan_end_date))
    table_scorecard = """
        <div class="ui five small statistics">
        <div class="grey statistic">
            <div class="value">"""+str(numberBets(jan_start_date, jan_end_date))+"""
            </div>
            <div class="grey label">
            No. Bets
            </div>
        </div>
            <div class="grey statistic">
                <div class="value">"""+str(totalProfit(jan_start_date, jan_end_date))+"""
                </div>
                <div class="label">
                Total Profit
                </div>
            </div> 
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountBet(jan_start_date, jan_end_date))+"""
            </div>
            <div class="label">
            Total Bet
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountWon(jan_start_date, jan_end_date))+"""
            </div>
            <div class="label">
            Total Won
            </div>
            </div>
            <div class="grey statistic">
            <div class="value">
            """+str(avgOdds(jan_start_date, jan_end_date))+"""
            </div>
            <div class="label">
            Avg Odds
            </div>
        </div>
        </div>"""

    table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""

    for index, row in df_monthly(jan_start_date, jan_end_date).iterrows():
        table_scorecard += """
    <div class="card"">   
        <div class=" content """+header_bg(row['BET_RESULT'])+"""">
                <div class=" header smallheader">"""+row['BET_PICK']+"""</div>
        <div class="meta smallheader">"""+str(row['BET_RESULT'])+"""</div>
        </div>
        <div class="content">
            <div class="description"><br>
                <div class="column kpi number">$"""+str(format(float(row['BET_AMOUNT']), '.2f'))+"""<br>
                    <p class="kpi text">Bet Amount</p>
                </div>
                <div class="column kpi number">$"""+str(format(float(row['BET_NET_PROFIT']), '.2f'))+"""<br>
                    <p class="kpi text">Net Profit</p>
                </div>
            </div>
        </div>
        <div class="extra content">
            <div class="meta"><i class="table icon"></i> BET Sport: """+str(row['BET_SPORT'])+"""</div>
            <div class="meta"><i class="user icon"></i> BET Source: """+str(row['BET_SOURCE'])+""" </div>
            <div class="meta"><i class="calendar alternate outline icon"></i> Bet Date: """+(row['BET_DATE'].strftime("%Y-%m-%d"))+"""</div>
        </div>
    </div>"""

    st.markdown(table_scorecard, unsafe_allow_html=True)

with tab_feb24:
    st.bar_chart(dailyProfit(feb_start_date, feb_end_date))
    table_scorecard = """
        <div class="ui five small statistics">
        <div class="grey statistic">
            <div class="value">"""+str(numberBets(feb_start_date, feb_end_date))+"""
            </div>
            <div class="grey label">
            No. Bets
            </div>
        </div>
            <div class="grey statistic">
                <div class="value">"""+str(totalProfit(feb_start_date, feb_end_date))+"""
                </div>
                <div class="label">
                Total Profit
                </div>
            </div> 
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountBet(feb_start_date, feb_end_date))+"""
            </div>
            <div class="label">
            Total Bet
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountWon(feb_start_date, feb_end_date))+"""
            </div>
            <div class="label">
            Total Won
            </div>
            </div>
            <div class="grey statistic">
            <div class="value">
            """+str(avgOdds(feb_start_date, feb_end_date))+"""
            </div>
            <div class="label">
            Avg Odds
            </div>
        </div>
        </div>"""

    table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""

    for index, row in df_monthly(feb_start_date, feb_end_date).iterrows():
        table_scorecard += """
    <div class="card"">   
        <div class=" content """+header_bg(row['BET_RESULT'])+"""">
                <div class=" header smallheader">"""+row['BET_PICK']+"""</div>
        <div class="meta smallheader">"""+str(row['BET_RESULT'])+"""</div>
        </div>
        <div class="content">
            <div class="description"><br>
                <div class="column kpi number">$"""+str(format(float(row['BET_AMOUNT']), '.2f'))+"""<br>
                    <p class="kpi text">Bet Amount</p>
                </div>
                <div class="column kpi number">$"""+str(format(float(row['BET_NET_PROFIT']), '.2f'))+"""<br>
                    <p class="kpi text">Net Profit</p>
                </div>
            </div>
        </div>
        <div class="extra content">
            <div class="meta"><i class="table icon"></i> BET Sport: """+str(row['BET_SPORT'])+"""</div>
            <div class="meta"><i class="user icon"></i> BET Source: """+str(row['BET_SOURCE'])+""" </div>
            <div class="meta"><i class="calendar alternate outline icon"></i> Bet Date: """+(row['BET_DATE'].strftime("%Y-%m-%d"))+"""</div>
        </div>
    </div>"""

    st.markdown(table_scorecard, unsafe_allow_html=True)

with tab_march24:
    st.bar_chart(dailyProfit(mar_start_date, mar_end_date))
    table_scorecard = """
        <div class="ui five small statistics">
        <div class="grey statistic">
            <div class="value">"""+str(numberBets(mar_start_date, mar_end_date))+"""
            </div>
            <div class="grey label">
            No. Bets
            </div>
        </div>
            <div class="grey statistic">
                <div class="value">"""+str(totalProfit(mar_start_date, mar_end_date))+"""
                </div>
                <div class="label">
                Total Profit
                </div>
            </div> 
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountBet(mar_start_date, mar_end_date))+"""
            </div>
            <div class="label">
            Total Bet
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">
            """+str(totalAmountWon(mar_start_date, mar_end_date))+"""
            </div>
            <div class="label">
            Total Won
            </div>
            </div>
            <div class="grey statistic">
            <div class="value">
            """+str(avgOdds(mar_start_date, mar_end_date))+"""
            </div>
            <div class="label">
            Avg Odds
            </div>
        </div>
        </div>"""

    table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""

    for index, row in df_monthly(mar_start_date, mar_end_date).iterrows():
        table_scorecard += """
    <div class="card"">   
        <div class=" content """+header_bg(row['BET_RESULT'])+"""">
                <div class=" header smallheader">"""+row['BET_PICK']+"""</div>
        <div class="meta smallheader">"""+str(row['BET_RESULT'])+"""</div>
        </div>
        <div class="content">
            <div class="description"><br>
                <div class="column kpi number">$"""+str(format(float(row['BET_AMOUNT']), '.2f'))+"""<br>
                    <p class="kpi text">Bet Amount</p>
                </div>
                <div class="column kpi number">$"""+str(format(float(row['BET_NET_PROFIT']), '.2f'))+"""<br>
                    <p class="kpi text">Net Profit</p>
                </div>
            </div>
        </div>
        <div class="extra content">
            <div class="meta"><i class="table icon"></i> BET Sport: """+str(row['BET_SPORT'])+"""</div>
            <div class="meta"><i class="user icon"></i> BET Source: """+str(row['BET_SOURCE'])+""" </div>
            <div class="meta"><i class="calendar alternate outline icon"></i> Bet Date: """+(row['BET_DATE'].strftime("%Y-%m-%d"))+"""</div>
        </div>
    </div>"""

    st.markdown(table_scorecard, unsafe_allow_html=True)