import json
import boto3


def lambda_handler(event, context):
    try:
        ev_id = event["queryStringParameters"]["ev_id"]

        print(ev_id)

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("ReStartCohort")
        item_val = "student_confirmations"
        response = table.scan()

        temp_table = response["Items"]

        response_confirm = []
        print(temp_table)

        student_confirm_item = temp_table[0]
        print(student_confirm_item.get("student_confirmations"))
        temp_stud = student_confirm_item.get("student_confirmations")

        for item in temp_stud:
            if item["event_id"] == ev_id:
                response_confirm.append(item)

        print(response_confirm)

        return {"statusCode": 200, "body": json.dumps(response_confirm)}
    except Exception as e:
        print(e)
