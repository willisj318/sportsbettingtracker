#from turtle import onclick
import streamlit as st
import pandas as pd
import statistics

#import streamlit.components.v1 as components
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
    )
# Initialize connection.
# Uses st.experimental_singleton to only run once.

# Set your Starting Bankroll
starting_bankroll = 96

df=pd.read_csv("./app/data/SB.csv")

df['BET_DATE'] = pd.to_datetime(df['BET_DATE'])
vegasdf = df[(df.BET_SOURCE == 'Vegas')]
acheungerdf = df[(df.BET_SOURCE == 'Acheunger')]
myselfdf = df[(df.BET_SOURCE == 'Myself')]
dailyprofitdf = df[['BET_DATE', 'BET_NET_PROFIT']]

df2 = df
# if 'df' not in st.session_state:
#    st.session_state.df = df

st.title('Data Visualization')

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

def numberBets():
    return(len(df.BET_ID))

def totalAmountBet():
    total_bet = sum(df.BET_AMOUNT)
    return(format(float(total_bet), '.2f'))

def totalAmountWon():
    total_won = sum(df.BET_GROSS_PROFIT)
    return(format(float(total_won), '.2f'))

def avgOdds():
    avg_odds = statistics.mean(df.BET_DECIMAL_ODDS)
    return(format(float(avg_odds), '.2F'))

def winningPercentage():
    return

def roi():
    #net profit / totalbets
    return()

def totalProfit():
    total_profit = sum(df.BET_NET_PROFIT)
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
    "Bet Source", fv_bet_source, len(fv_bet_source)-1, key=st.session_state.selectbox_bet_source_key)

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

# Bet Date Range
fv_owner = df['BET_DATE'].drop_duplicates()
fv_owner = pd.concat([fv_owner,all_option])
selectbox_date = st.sidebar.selectbox(
    "Bet Date", fv_owner, len(fv_owner)-1, key=st.session_state.selectbox_bet_date_key)

if selectbox_date != 'All':
    df = df.loc[df['BET_DATE'] > selectbox_date]
else:
    df = df.loc[df['BET_DATE'].isin(fv_owner)]

# Filter Session Reset
def reset_button():
    st.session_state.selectbox_database_key = st.session_state.selectbox_database_key+1
    st.session_state.selectbox_bet_type_key = st.session_state.selectbox_bet_type_key+1
    st.session_state.selectbox_bet_source_key = st.session_state.selectbox_bet_source_key+1
    st.session_state.selectbox_bet_sport_key = st.session_state.selectbox_bet_sport_key+1
    st.session_state.selectbox_bet_date_key = st.session_state.selectbox_bet_date_key+1
    st.session_state.selectbox_sb_key = st.session_state.selectbox_sb_key+1


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

df.sort_values(by=[orderby_column], inplace=True, ascending=orderby_asc)

# df[(df.FULL_NAME == player_selction) & (df.TOURNAMENT_DATE.dt.date > date_selction)]

def calculate_daily_bankroll():
    df_daily = df[['BET_DATE', 'BET_NET_PROFIT']]
    df_daily.insert(2, "DAILY_BR", [starting_bankroll, df_daily.groupby(['BET_DATE']).cumsum()])
    st.write(df_daily.groupby(['BET_DATE']).cumsum())

profit_by_day = df.groupby(df.BET_DATE)['BET_NET_PROFIT'].sum()
profit_by_sport = df.groupby(df.BET_SPORT)['BET_NET_PROFIT'].sum()
rolling_bankroll = df.groupby(df.BET_DATE)['BET_NET_PROFIT'].sum() + starting_bankroll

# Set Layout

st.write('Starting Bankroll: ', starting_bankroll)
#st.write('Current Bankroll: ', format(float(starting_bankroll + df['BET_NET_PROFIT'].sum()), '.2f'))

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(profit_by_day)
    st.bar_chart(profit_by_sport)

with col2:
    st.line_chart(profit_by_day)
    st.write('loser')

calculate_daily_bankroll()    