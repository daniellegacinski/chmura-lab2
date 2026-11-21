import html
import os

import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["TEMPLATE_BUCKET"]
KEY = os.environ.get("TEMPLATE_KEY", "template.html")


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    imie = (params.get("imie") or "").strip()

    if not imie:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": "Brak parametru 'imie'. Użyj np.: ?imie=Anna",
        }

    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    template = obj["Body"].read().decode("utf-8")

    body = template.replace("{{IMIE}}", html.escape(imie))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": body,
    }