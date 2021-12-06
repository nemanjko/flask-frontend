from dynamodb_utils import \
    collect_current_data, \
    add_new_symbol, \
    get_data, \
    control_trading, \
    activate_symbol, \
    remove_symbol

def get_settings_data(request, dynamodb):
    data = {}
    if request.method == 'POST':
        our_symbol = request.form['our_symbol']
        new_symbol = request.form['symbol']
        new_rsi = request.form['rsi']
        if our_symbol.strip() != '' and new_symbol.strip() != '' and new_rsi.strip() != '':
            add_new_symbol(dynamodb, our_symbol, new_symbol, new_rsi)
    elif request.method == 'GET':
        command = request.args.get('command')
        if command is None:
            trading_running = int(get_data(dynamodb, "TRADING#RUNNING")['Item']['pk_value']['N'])
            if trading_running == 1:
                data["trading"] = 'stop'
            else:
                data["trading"] = 'start'
        elif command == 'stop':
            control_trading(dynamodb, 0)
            data["trading"] = "start"
        elif command == 'start':
            control_trading(dynamodb, 1)
            data["trading"] = "stop"
        elif command == 'activate':
            symbol = request.args.get('symbol')
            if '-' in symbol:
                symbol = symbol.replace('-', '#')
                activate_symbol(dynamodb, symbol, 1)
        elif command == 'deactivate':
            symbol = request.args.get('symbol')
            if '-' in symbol:
                symbol = symbol.replace('-', '#')
                activate_symbol(dynamodb, symbol, 0)
        elif command == 'remove':
            symbol = request.args.get('symbol')
            if '-' in symbol:
                symbol = symbol.replace('-', '#')
                remove_symbol(dynamodb, symbol)
    data["traded_coins_list"] = get_coin_data_array(dynamodb)
    return data

def get_coin_data_array(dynamodb):
    coin_data_array = []
    active_coins = collect_current_data(dynamodb, 1)
    inactive_coins = collect_current_data(dynamodb, 0)
    all_coins = active_coins['Items'] + inactive_coins['Items']
    for coin in all_coins:
        coin_data_json = {'symbol': coin['pk']['S'], 'rsi': coin['rsi_interval']['S'],
                          'status': coin['analysis_status']['S']}
        if 'quantity' in coin:
            coin_data_json['quantity'] = coin['quantity']['N']
        else:
            coin_data_json['quantity'] = 0
        coin_data_json['active'] = coin['active']['N']
        if 'profit' in coin:
            coin_profit = coin['profit']['N']
            coin_data_json['profit'] = coin_profit
        else:
            coin_data_json['profit'] = 0
        coin_data_array.append(coin_data_json)
    return coin_data_array
