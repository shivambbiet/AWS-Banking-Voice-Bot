import boto3
import random
import json
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerOTPTable')
sns = boto3.client('sns')

def generate_otp():
    return str(random.randint(100000, 999999))

def lambda_handler(event, context):
    """
    Triggered by Amazon Lex/Connect to generate and verify OTP
    for banking customer authentication.
    """
    intent = event.get('sessionState', {}).get('intent', {}).get('name')
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})

    if intent == 'SendOTP':
        phone_number = slots.get('PhoneNumber', {}).get('value', {}).get('interpretedValue')
        otp = generate_otp()
        expiry = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

        table.put_item(Item={
            'phone_number': phone_number,
            'otp': otp,
            'expiry': expiry,
            'verified': False
        })

        sns.publish(
            PhoneNumber=phone_number,
            Message=f"Your verification code is {otp}. Valid for 5 minutes."
        )

        return build_response("OTP sent successfully. Please enter the code.")

    elif intent == 'VerifyOTP':
        phone_number = slots.get('PhoneNumber', {}).get('value', {}).get('interpretedValue')
        entered_otp = slots.get('OTPCode', {}).get('value', {}).get('interpretedValue')

        response = table.get_item(Key={'phone_number': phone_number})
        item = response.get('Item')

        if not item:
            return build_response("No OTP request found. Please request a new code.")

        if datetime.utcnow().isoformat() > item['expiry']:
            return build_response("OTP expired. Please request a new one.")

        if item['otp'] == entered_otp:
            table.update_item(
                Key={'phone_number': phone_number},
                UpdateExpression="SET verified = :v",
                ExpressionAttributeValues={':v': True}
            )
            return build_response("Verification successful. How can I help you today?")
        else:
            return build_response("Incorrect OTP. Please try again.")


def build_response(message):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"state": "Fulfilled"}
        },
        "messages": [{"contentType": "PlainText", "content": message}]
    }
