#from turtle import onclick
import streamlit as st
import pandas as pd
import datetime
from csv import writer

#import streamlit.components.v1 as components
st.set_page_config(
    page_title="Submit Picks",
    layout="wide"
    )
# Initialize connection.
# Uses st.experimental_singleton to only run once.

### CSV File ###
filename = "./app/data/SB.csv"

st.title('Submit Bets')

def sports_bet_insert(bet_date, bet_type, bet_result, bet_pick, bet_source, bet_amount, bet_sport, bet_odds, bet_boost_used, bet_odds_before_boost, bet_sb_used, bet_bonus_bet):
    print('Starting Post Requst')

    if bet_result == 'Win':
        gross_profit = format(float(bet_amount) * float(bet_odds), '.2f')
        net_profit = format(float(gross_profit) - float(bet_amount), '.2f')
        print('You are in the green', gross_profit)
        print(('net profit was ', net_profit))
    else:
        gross_profit = format(float(bet_amount) * 0, '.2f')
        net_profit = format(float(gross_profit) - float(bet_amount), '.2f')
        print('You are in the red', gross_profit)

    bet_id_read = pd.read_csv("./app/data/SB.csv")
    bet_count= len(bet_id_read)
    
    BET_ID = bet_count + 1

    updates = [BET_ID, bet_date, bet_type, bet_result, bet_pick, bet_source, bet_amount, bet_sport, bet_odds, bet_odds_before_boost, net_profit, bet_boost_used, gross_profit, bet_sb_used, bet_bonus_bet]

    with open (filename, 'a', newline='') as fd:
        writer_object = writer(fd)
        writer_object.writerow(updates)
        fd.close()

with st.form("submitpicks"):
    bet_date = st.date_input("Date of Pick", datetime.date(2024, 2, 29))
    bet_pick = title = st.text_input('Bet Pick', 'e.g. Cavs @ Mavs U225.5')
    bet_source = st.selectbox(
        'Bet Source',
        ('Myself', 'Vegas', 'TexasToast', 'Finnedai', 'Ace', 'Manu', 'Cometknight', 'Acheunger')
    )
    bet_sport = st.selectbox(
        'Bet Sport',
        ('NBA', 'NFL', 'NCAAF', 'NHL', 'NCAAB', 'Soccer', 'Golf')
    )
    bet_odds = title = st.text_input('Decimal Odds', '2.00')
    bet_amount = title = st.text_input('Bet Amount', '5.00')
    bet_boost_used = st.selectbox(
        'Boost Used',
        ('No', 'Yes') 
    )
    bet_odds_before_boost = title = st.text_input('Odds Before Boost', '0')
    bet_type = st.selectbox(
        'Bet Type',
        ('Moneyline', 'Spread', 'Prop', 'Parlay', 'Over/Under')
    )
    bet_result = st.selectbox(
        'Bet Result',
        ('Pending', 'Win', 'Loss', 'Draw', 'Cashout', 'Other')
    )
    bet_sb_used = st.selectbox(
        'Sportsbook',
        ('Fanduel', 'Draftkings', 'Bet 365', 'BetUS', 'Other')
    )
    bet_bonus_bet = st.selectbox(
        'Bonus Bet',
        ('No', 'Yes') 
    )

    submitted = st.form_submit_button("Submit")
    if submitted:
        sports_bet_insert(bet_date, bet_type, bet_result, bet_pick, bet_source, bet_amount, bet_sport, bet_odds, bet_boost_used, bet_odds_before_boost, bet_sb_used, bet_bonus_bet)