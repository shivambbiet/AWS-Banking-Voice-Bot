import boto3

dynamodb = boto3.resource('dynamodb')
accounts_table = dynamodb.Table('CustomerAccountsTable')

def lambda_handler(event, context):
    """
    Validates customer account details after OTP verification.
    Checks account existence and status in DynamoDB.
    """
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    account_number = slots.get('AccountNumber', {}).get('value', {}).get('interpretedValue')

    response = accounts_table.get_item(Key={'account_number': account_number})
    account = response.get('Item')

    if not account:
        message = "Account not found. Please check the account number and try again."
    elif account.get('status') != 'active':
        message = "This account is currently inactive. Please contact customer support."
    else:
        balance = account.get('balance')
        message = f"Account validated. Your current balance is ${balance}."

    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"state": "Fulfilled"}
        },
        "messages": [{"contentType": "PlainText", "content": message}]
    }
