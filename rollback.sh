#!/bin/bash
export AWS_PROFILE=ntnu

account_id=391035843039
region=us-east-1

# Remove DynamoDB table
aws dynamodb delete-table --table-name cnTable

# Remove Lambda functions
aws lambda delete-function --function-name cnGetFunction
aws lambda delete-function --function-name cnPutFunction
aws lambda delete-function --function-name cnDeleteFunction

# Remove API, replace some_api_id with id of your API
aws apigateway delete-rest-api --rest-api-id rd0cpvjm3l

# Remove IAM policies and roles
aws iam delete-role-policy --role-name cnRole --policy-name cnPolicy
aws iam detach-role-policy --role-name cnRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name cnRole