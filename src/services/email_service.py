import datetime
import json
import boto3
from src.util.config import ConfigValues
from src.util import templates

ses_client = boto3.client('ses')
dynamo_client = boto3.resource('dynamodb')

def list_subscribers():
    table = dynamo_client.Table(ConfigValues.SUBSCRIBER_TABLE)

    results = table.scan(
        Select = "ALL_ATTRIBUTES"
    )

    # Pull out all of the email addressed (filtering out unsubscribed users)
    return [r['SubscriberEmail'] for r in results['Items'] if r['Status'] == 'subscribed']

def add_subscription(email):
    """Adds a new user to our subscriber list and sends out a confirmation"""
    _validate_email(email)

    # Add to dynamo
    _create_subscriber(email)

    # Send confirmation
    send_email(email,
        subject=f"You're subscribed to {ConfigValues.TITLE}!",
        template='email/sub_confirmation.html',
        data={
            'email': email
        }, bcc=ConfigValues.SUB_CONFIRM_BCC.split(',')
    )

def remove_subscription(email):
    """Removes a user from our subscriber list"""
    _validate_email(email)

    _update_subscriber(email, 'unsubscribed')

def send_email(email, subject, template, data, bcc=None):
    """Sends out a templated email using SES"""
    if data is None:
        data = {}

    data['unsubscribe_link'] = f"{ConfigValues.HOMEPAGE}/unsubscribe?email={email}"

    return ses_client.send_email(
        Source = f"{ConfigValues.TITLE} <{ConfigValues.CONTACT_EMAIL}>",
        Destination = {
            "ToAddresses": [email],
            "BccAddresses": bcc if bcc else [],
        },
        Message = {
            "Subject": {
                "Charset": "UTF-8",
                "Data": subject
            },
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": templates.render(template, data)
                }
            }
        }
    )

def _validate_email(email):
    # First we do some simple validation, don't go too crazy because emails come
    # in a bazillion formats
    email_parts = email.split('@')
    if len(email_parts) != 2:
        raise ValueError("Email must contain one @")
    if '.' not in email_parts[1]:
        raise ValueError("Email must contain a period after the @")

def _create_subscriber(email):
    """Write new contact to Dynamo"""
    table = dynamo_client.Table(ConfigValues.SUBSCRIBER_TABLE)

    # Note that the default behavior is to override
    return table.put_item(Item={
        'SubscriberEmail': email,
        'CreatedAt': datetime.datetime.utcnow().isoformat(),
        'UpdatedAt': datetime.datetime.utcnow().isoformat(),
        'Status': 'subscribed',
    })

def _update_subscriber(email, status):
    """Update a subscription to the provided status (used for unsubscribing users)"""
    table = dynamo_client.Table(ConfigValues.SUBSCRIBER_TABLE)

    return table.update_item(
      Key = {
        "SubscriberEmail": email,
      },
      UpdateExpression = "set #s = :status, #u = :updatedAt",
      ExpressionAttributeValues = {
        ":status": status,
        ":updatedAt": datetime.datetime.utcnow().isoformat(),
      },
      ExpressionAttributeNames = {
        "#s": "Status",
        "#u": "UpdatedAt",
      },
      ReturnValues = "UPDATED_NEW"
    )
