#!/bin/bash
export AWS_PROFILE=default

account_id=XXXXXXXXXXX #Edit with your AWS ACCOUNT ID
region=us-east-1
rest_api_id=93q5r8f7ac #Edit with relevant AWS API ID

# Remove DynamoDB table
aws dynamodb delete-table --table-name cnTable

# Remove Lambda functions
aws lambda delete-function --function-name cnGetFunction
aws lambda delete-function --function-name cnPutFunction
aws lambda delete-function --function-name cnDeleteFunction

# Remove API, replace some_api_id with id of your API
aws apigateway delete-rest-api --rest-api-id $rest_api_id

# Remove IAM policies and roles
aws iam delete-role-policy --role-name cnRole --policy-name cnPolicy
aws iam detach-role-policy --role-name cnRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name cnRole

# Empty S3 bucket
aws s3 rm s3://api-honeypot-logs --recursive
# Remove S3 bucket
aws s3api delete-bucket \
    --bucket api-honeypot-logs \
    --region us-east-1
