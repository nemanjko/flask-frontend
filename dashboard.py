
def get_dashboard_data():
    data = {"labels": "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']",
            "chart_values": """
              {data: 
                 [
                    "34",
                    "67",            
                    "140",
                    "17",
                    "55",
                    "312",
                    "230",
                    "535",
                    "30",
                    "9",
                    "5",
                    "44",
                 ],
              label: 'profit per month',
              borderColor: '#3e95cd',
              fill: true}
           """, "remaining_cash": 478}

    data["traded_coins_numb"] = 4
    data["traded_coins_list"] = [
        {'symbol': "BTC", 'rsi': "1m", 'status': "watching", 'quantity':2, 'active':1, 'profit':200},
        {'symbol': "ETH", 'rsi': "15m", 'status': "buying", 'quantity':5, 'active':1, 'profit':300},
        {'symbol': "XRP", 'rsi': "15m", 'status': "selling", 'quantity':1500, 'active':1, 'profit':30},
        {'symbol': "BNB", 'rsi': "1h", 'status': "selling", 'quantity':50, 'active':1, 'profit':2}
    ]
    data["total_profit"] = 532
    return data

