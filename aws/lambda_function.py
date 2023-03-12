import json
import base64
import boto3


# モデルのエンドポイント
CRAFT_ENDPOINT = "pytorch-inference-xxxx-xx-xx-xx-xx-xx-xxx"


def craft(client, image_bytes:bytes):
    # composite
    rawdata = image_bytes
    
    response = client.invoke_endpoint(
        EndpointName=CRAFT_ENDPOINT,
        ContentType="application/x-npy",
        Accept="application/json",
        Body=rawdata,
    )
    
    bboxes = json.loads(response["Body"].read())
    
    return bboxes


def lambda_handler(event, context):
    try:
        # get params
        image_bytes = base64.b64decode(event["image_bytes"].encode("utf8"))
        
        # segemaker
        client = boto3.client("sagemaker-runtime")
        
        # image to chars bbox
        bboxes = craft(client, image_bytes)
        
        return {
            "statusCode": 200,
            "body": {"bboxes":bboxes},
        }
    except Exception as e:
        return {
            "statusCode": 404,
            "body": str(e),
        }
