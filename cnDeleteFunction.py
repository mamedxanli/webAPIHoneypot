import json

def lambda_handler(event, context):
    return {
        'statusCode': 400,
        'body': json.dumps('One or more parameter values are not valid! Please, use correct formatting!')
}

