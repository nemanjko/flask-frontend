from dynamodb_utils import get_data, collect_current_data

def get_dashboard_data(dynamodb):
    data = {"labels": "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']",
            "chart_values": """
              {data: 
                 [
                    """ + str(get_data(dynamodb, "PROFIT#JAN")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#FEB")['Item']['pk_value']['N']) + """,            
                    """ + str(get_data(dynamodb, "PROFIT#MAR")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#APR")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#MAY")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#JUN")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#JUL")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#AUG")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#SEP")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#OCT")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#NOV")['Item']['pk_value']['N']) + """,
                    """ + str(get_data(dynamodb, "PROFIT#DEC")['Item']['pk_value']['N']) + """,
                 ],
              label: 'profit per month',
              borderColor: '#3e95cd',
              fill: true}
           """, "remaining_cash": get_data(dynamodb, "CASH")['Item']['pk_value']['N']}

    total_profit = 0
    coin_data_array = []
    active_coins = collect_current_data(dynamodb, 1)
    for active_coin in active_coins['Items']:
        coin_data_json = {'symbol': active_coin['pk']['S'], 'rsi': active_coin['rsi_interval']['S'],
                          'status': active_coin['analysis_status']['S']}
        if 'quantity' in active_coin:
            coin_data_json['quantity'] = active_coin['quantity']['N']
        else:
            coin_data_json['quantity'] = 0
        coin_data_json['active'] = active_coin['active']['N']
        if 'profit' in active_coin:
            coin_profit = active_coin['profit']['N']
            coin_data_json['profit'] = coin_profit
            total_profit = total_profit + coin_profit
        else:
            coin_data_json['profit'] = 0
        coin_data_array.append(coin_data_json)

    data["traded_coins_numb"] = len(active_coins['Items'])
    data["traded_coins_list"] = coin_data_array
    data["total_profit"] = total_profit
    return data
