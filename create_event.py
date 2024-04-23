import json
import boto3
from urllib.parse import quote


def lambda_handler(event, context):
    try:
        client = boto3.client("sns")
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("ReStartCohort")
        item_json = json.dumps(event)

        item_data = json.loads(item_json)
        print(item_json)

        # calling function to publish data
        sns_pub_response = sns_publish(client, item_data)

        # Checking the DynamoDB for exisiting event list
        get_resp = table.get_item(
            Key={"cohort": "AWS RE/START", "batch": "events"},
        )

        item_exist = get_resp["Item"]["event_name"]

        if not item_exist:
            item_exist = []
        item_exist.append(item_data)

        # Updating the DynamoDB
        response = table.update_item(
            Key={"cohort": "AWS RE/START", "batch": "events"},
            UpdateExpression="SET event_name = :s",
            ExpressionAttributeValues={":s": item_exist},
            ReturnValues="UPDATED_NEW",
        )
        print(response)

        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        print(e)


def sns_publish(client, item_data):

    url_to_encode = (
        "http://confirm-attendance-app.s3-website-us-east-1.amazonaws.com?e_id="
        + item_data["event_id"]
        + "&e_loc="
        + quote(item_data["Location"])
        + "&e_title="
        + quote(item_data["Title"])
        + "&e_date="
        + item_data["Date"]
        + "&e_time="
        + item_data["Time"]
    )

    sns_message = (
        "Upcoming event: "
        + item_data["Title"]
        + ", Location: "
        + quote(item_data["Location"])
        + ", Date : "
        + item_data["Date"]
        + ", Time : "
        + item_data["Time"]
        + ".\n\n Please click the following link to confirm your attendance:\n\n"
        + url_to_encode
    )

    #'Upcoming event: ' + item_data['Title'] + ', Location: ' + item_data['Location'] + ', Date : ' + item_data['Date'] + ', Time : ' + item_data['Time']

    # SNS Notification creation
    sns_response = client.publish(
        TopicArn="arn:aws:sns:us-east-1:339713081414:reStartEventNotifications",
        Subject="AWS re/Start Event Notification",
        Message=sns_message,
    )
    return sns_response
