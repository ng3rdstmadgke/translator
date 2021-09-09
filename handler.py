import json
import boto3
import os

def translate(event, context):
    b = event["body"]
    req_body = json.loads(b)
    src_lang = req_body.get("src_lang", "auto")
    dst_lang = req_body.get("dst_lang", "ja")
    text     = req_body.get("text", "")

    response_body = {
        "request": {
            "text": text,
            "src_lang": src_lang,
            "dst_lang": dst_lang,
        },
        "result": {
            "text": "",
            "src_lang": "auto",
            "dst_lang": "ja",
        }
    }
    if ("text" not in req_body):
        return {
            "statusCode": 200,
            "headers": { "content-type": "application/json" },
            "body": json.dumps(response_body)
        }

    translate = boto3.client(service_name='translate', region_name='ap-northeast-1', use_ssl=True)
    result = translate.translate_text(
        Text=text,
        SourceLanguageCode=src_lang,
        TargetLanguageCode=dst_lang
    )
    response_body["result"]["text"] = result["TranslatedText"]
    response_body["result"]["src_lang"] = result["SourceLanguageCode"]
    response_body["result"]["dst_lang"] = result["TargetLanguageCode"]
    response = {
        "statusCode": 200,
        "headers": { "content-type": "application/json" },
        "body": json.dumps(response_body)
    }
    return response

def static(event, context):
    path = "." + os.path.abspath(event["path"])
    if (not path.startswith("./static")):
        return { "statusCode": 404 }
    if (os.path.isdir(path)):
        path = os.path.join(path, "index.html")
    if (not os.path.isfile(path)):
        return { "statusCode": 404 }

    if (path.endswith(".css")):
        content_type = "text/css"
    elif (path.endswith(".js")):
        content_type = "text/javascript"
    elif (path.endswith(".json")):
        content_type = "application/json"
    else:
        content_type = "text/html"

    with open(path) as f:
        body = f.read()

    response = {
        "headers": {
            "content-type": content_type
        },
        "body": body
    }

    return response
