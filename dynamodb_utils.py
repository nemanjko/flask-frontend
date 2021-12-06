import requests

def get_data(dynamodb, pk):
    item = dynamodb.get_item(
        TableName='CryptoBotTraderTable',
        Key={
            'pk': {"S": pk}
        }
    )
    return item

def collect_current_data(dynamodb, active):
    items = dynamodb.query(
        TableName='CryptoBotTraderTable',
        IndexName='active_coins',
        KeyConditionExpression='active = :a',
        ScanIndexForward=False,
        ExpressionAttributeValues={
            ':a': {'N': str(active)}
        })
    return items


def control_trading(dynamodb, command):
    dynamodb.update_item(
        TableName='CryptoBotTraderTable',
        Key={
            'pk': {"S": 'TRADING#RUNNING'}
        },
        UpdateExpression="set pk_value=:vl",
        ExpressionAttributeValues={
            ':vl': {"N": str(command)}
        }
    )

def activate_symbol(dynamodb, symbol, active):
    dynamodb.update_item(
        TableName='CryptoBotTraderTable',
        Key={
            'pk': {"S": symbol}
        },
        UpdateExpression="set active=:ac",
        ExpressionAttributeValues={
            ':ac': {"N": str(active)}
        }
    )


def remove_symbol(dynamodb, symbol):
    dynamodb.delete_item(
        TableName='CryptoBotTraderTable',
        Key={
            'pk': {"S": symbol}
        }
    )


def add_new_symbol(dynamodb, our_symbol, coin_symbol, rsi_interval):
    lot_size = get_lot_size(coin_symbol)
    if lot_size > -1:
        dynamodb.put_item(
            TableName='CryptoBotTraderTable',
            Item={
                'pk': {
                    'S': str(our_symbol)
                },
                'active': {
                    'N': '1'
                },
                'lot_size': {
                    'N': str(lot_size)
                },
                'analysis_status': {
                    'S': "watching for entry"
                },
                'rsi_interval': {
                    'S': str(rsi_interval)
                },
                'symbol': {
                    'S': str(coin_symbol)
                },
                'base_symbol': {
                    'S': 'USDT'
                }
            }
        )

def get_lot_size(symbol):
   lot_size = -1
   response = requests.get('https://api.binance.com/api/v3/exchangeInfo?symbol=' + symbol + 'USDT')
   print(response)
   for i in range(0, len(response.json()['symbols'])):
      print(response.json()['symbols'][i]['symbol'])
      if response.json()['symbols'][i]['symbol'] == (symbol + 'USDT'):
         filters = response.json()['symbols'][i]['filters']
         print(filters)
         for j in range(0, len(filters)):
            if response.json()['symbols'][i]['filters'][j]['filterType'] == 'LOT_SIZE':
               lot_size = count_zero_in_decimal_number(float(response.json()['symbols'][i]['filters'][j]['stepSize']))+1
   return lot_size


def count_zero_in_decimal_number(number):
    zeros = 0
    while number < 0.1:
        number *= 10
        zeros += 1
    return zeros
