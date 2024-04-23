import json
import boto3


def lambda_handler(event, context):
    try:

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("ReStartCohort")
        item_json = json.dumps(event)

        item_data = json.loads(item_json)
        print(item_json)

        # Checking the DynamoDB for exisiting event list
        get_resp = table.get_item(
            Key={"cohort": "AWS RE/START", "batch": "confirm"},
        )

        item_exist = get_resp["Item"]["student_confirmations"]

        if not item_exist:
            item_exist = []
        item_exist.append(item_data)

        # Updating the DynamoDB
        response = table.update_item(
            Key={"cohort": "AWS RE/START", "batch": "confirm"},
            UpdateExpression="SET student_confirmations = :s",
            ExpressionAttributeValues={":s": item_exist},
            ReturnValues="UPDATED_NEW",
        )
        print(response)

        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        print(e)
