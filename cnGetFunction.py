import json

def lambda_handler(event, context):
    return {
        'statusCode': 400,
        'body': json.dumps('"errorMessage": "An error occurred (ValidationException) when calling the GetItem operation: One or more parameter values are not valid!')
    }

