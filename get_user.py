import json
import boto3


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("ReStartCohort")

        resp_student = table.get_item(
            Key={"cohort": "AWS RE/START", "batch": "student_list"},
        )

        response = resp_student["Item"]["details"]
        print(response)

        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        print(e)
