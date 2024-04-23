import json
import boto3


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("ReStartCohort")

        response = table.get_item(
            Key={"cohort": "AWS RE/START", "batch": "events"},
        )
        print(response)
        print(response["Item"])
        event_list = response["Item"]["event_name"]
        return {"statusCode": 200, "body": json.dumps(event_list)}
    except Exception as e:
        print(e)
