#!/bin/bash
: ' export environmental variables, setting region, aws_access_key_id and aws_secret_access_key. It is assumed that you have AWS account with relevant permissions, and downloaded, installed and configure AWS CLI package. For the simplicity in the test environment you can use AWS root account, although it is not recommended to use root account for production environment.

Example ~/.aws/config file:
[profile ntnu]
region = us-east-1
output = json

Example ~/.aws/credentials file:
[ntnu]
aws_access_key_id = some_access_key_id
aws_secret_access_key = some_access_key

IMPORTANT! Do not run this script against AWS account, where you have other resources. This code is a part of solution presented in a Master Thesis by Alakbar Mammadov at NTNU. Create a separate AWS account for this experiment and make sure you do not have any important resources under that account.

The following line exports credentials, making them avaiable for shell script, thus avoiding typing in region, aws_access_key_id, aws_secret_access_key in every command. '

export AWS_PROFILE=ntnu

resource_name=testpath
echo "Setting API resource name: " $testpath 

account_id=391035843039
region=us-east-1
first_arn=arn:aws:apigateway:$region:lambda:path/2015-03-31/functions

echo "Setting account ID: " $account_id
echo "Setting your region: " $region
echo "Creating DynamoDB database"

aws dynamodb create-table \
--table-name cnTable \
--attribute-definitions AttributeName=id,AttributeType=S \
--key-schema AttributeName=id,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

sleep 3

echo "Creating IAM role and assume trust policy"
aws iam create-role \
    --role-name cnRole \
    --assume-role-policy-document file://trust.json
sleep 3

echo "Attaching inline IAM policy to the role created"
aws iam put-role-policy \
    --role-name cnRole \
    --policy-name cnPolicy \
    --policy-document file://inline_policy_dynamodb.json
sleep 3

echo "Attaching Lambda execution role policy"
aws iam attach-role-policy \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
    --role-name cnRole

echo "Waiting 20 seconds before all roles and policies are created"
sleep 20

echo "Zipping files with Python functions"
zip -r9 cnGetFunction.zip cnGetFunction.py
zip -r9 cnPutFunction.zip cnPutFunction.py
zip -r9 cnDeleteFunction.zip cnDeleteFunction.py
sleep 3

#Getting arn for the role:
role_arn=$(aws iam get-role --role-name cnRole | jq -r '.Role.Arn')

echo "Creating Lambda function for REST GET call" 
aws lambda create-function \
    --function-name cnGetFunction \
    --runtime python3.9 \
    --zip-file fileb://cnGetFunction.zip \
    --handler cnGetFunction.lambda_handler \
    --role $role_arn
sleep 3

echo "Creating Lambda function for REST PUT call"
aws lambda create-function \
    --function-name cnPutFunction \
    --runtime python3.9 \
    --zip-file fileb://cnPutFunction.zip \
    --handler cnPutFunction.lambda_handler \
    --role $role_arn
sleep 3
echo "Creating Lambda function for REST DELETE call"




aws lambda create-function \
    --function-name cnDeleteFunction \
    --runtime python3.9 \
    --zip-file fileb://cnDeleteFunction.zip \
    --handler cnDeleteFunction.lambda_handler \
    --role $role_arn
sleep 3

echo "Creating API Gateway"
rest_api_id=$(aws apigateway create-rest-api --name 'testAPI' | jq -r '.id')
sleep 5
parent_id=$(aws apigateway get-resources --rest-api-id $rest_api_id | jq -r '.items[].id')
aws apigateway create-resource --rest-api-id $rest_api_id --parent-id $parent_id --path-part $resource_name
id_list=$(aws apigateway get-resources --rest-api-id $rest_api_id | jq -r '.items[] | .id')

for i in $id_list; do \ 
	if [[ ${#i} -lt 9 ]]; then \
        resource_id=$i; \
	fi \
done > /dev/null

sleep 5
echo "Creating GET method and setting request settings"
aws apigateway put-method \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method GET \
        --authorization-type "NONE" \
        --no-api-key-required \
        --request-parameters '{"method.request.querystring.id" : true}'
sleep 5
#Getting GET Lambda function arn:
get_arn=$(aws lambda get-function --function-name cnGetFunction | jq -r '.Configuration.FunctionArn')

echo "Setting integration request settings for GET method"
aws apigateway put-integration \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method GET \
	--integration-http-method POST \
	--uri $first_arn/$get_arn/invocations \
	--type AWS \
	--passthrough-behavior WHEN_NO_TEMPLATES \
	--request-templates '{ "application/json": "{\"id\": \"$input.params('\''id'\'')\"}"}'
sleep 5

echo "Updating method response settings for GET method"
aws apigateway put-method-response \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method GET \
	--status-code 200 \
	--response-models '{"application/json" : "Empty"}'
	
sleep 5
echo "Updating integration response settings for GET method"
aws apigateway put-integration-response \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method GET \
        --status-code 200 \
	--selection-pattern "-"

sleep 5
echo "Creating PUT method and setting request settings"
aws apigateway put-method \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method PUT \
        --authorization-type "NONE" \
        --no-api-key-required \
        --request-parameters '{"method.request.querystring.id":true, "method.request.querystring.City": true, "method.request.querystring.Model":true, "method.request.querystring.Output":true, "method.request.querystring.PostCode":true, "method.request.querystring.SN":true, "method.request.querystring.Street":true}'

sleep 5

put_arn=$(aws lambda get-function --function-name cnPutFunction | jq -r '.Configuration.FunctionArn')
echo "Updating integration request settings for PUT method"
aws apigateway put-integration \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method PUT \
	--integration-http-method POST \
	--uri $first_arn/$put_arn/invocations \
	--type AWS \
	--passthrough-behavior WHEN_NO_TEMPLATES \
	--request-templates '{ "application/json": "{\"id\": \"$input.params('\''id'\'')\",\"City\": \"$input.params('\''City'\'')\",\"Model\": \"$input.params('\''Model'\'')\",\"Output\": \"$input.params('\''Output'\'')\",\"PostCode\": \"$input.params('\''PostCode'\'')\",\"SN\": \"$input.params('\''SN'\'')\",\"Street\": \"$input.params('\''Street'\'')\" }"}'
sleep 5
echo "Updating method response settings for PUT method"
aws apigateway put-method-response \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method PUT \
	--status-code 200 \
	--response-models '{"application/json" : "Empty"}'

sleep 5
echo "Updating integration response settings for PUT method"
aws apigateway put-integration-response \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method PUT \
        --status-code 200 \
	--selection-pattern "-"

sleep 5
echo "Creating DELETE method and setting request settings"
aws apigateway put-method \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method DELETE \
        --authorization-type "NONE" \
        --no-api-key-required \
        --request-parameters '{"method.request.querystring.id" : true}'

sleep 5

delete_arn=$(aws lambda get-function --function-name cnDeleteFunction | jq -r '.Configuration.FunctionArn')
echo "Setting integration request settings for DELETE method"
aws apigateway put-integration \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method DELETE \
	--integration-http-method POST \
	--uri $first_arn/$delete_arn/invocations \
	--type AWS \
	--passthrough-behavior WHEN_NO_TEMPLATES \
	--request-templates '{ "application/json": "{\"id\": \"$input.params('\''id'\'')\"}"}'
sleep 5
echo "Updating method response settings for DELETE method"
aws apigateway put-method-response \
	--rest-api-id $rest_api_id \
	--resource-id $resource_id \
	--http-method DELETE \
	--status-code 200 \
	--response-models '{"application/json" : "Empty"}'
sleep 5
echo "Updating integration response settings for DELETE method"
aws apigateway put-integration-response \
        --rest-api-id $rest_api_id \
        --resource-id $resource_id \
        --http-method DELETE \
        --status-code 200 \
	--selection-pattern "-"

sleep 3
echo "Adding permissions to the GET function"
aws lambda add-permission \
    --function-name cnGetFunction \
    --action lambda:InvokeFunction \
    --statement-id get_func_statement_id-1 \
    --principal apigateway.amazonaws.com \
	--source-arn arn:aws:execute-api:$region:$account_id:$rest_api_id/*/GET/$resource_name

echo "Adding permissions to the PUT function"
aws lambda add-permission \
    --function-name cnPutFunction \
    --action lambda:InvokeFunction \
    --statement-id put_func_statement_id-1 \
    --principal apigateway.amazonaws.com \
    --source-arn arn:aws:execute-api:$region:$account_id:$rest_api_id/*/PUT/$resource_name

echo "Adding permissions to the DELETE function"
aws lambda add-permission \
    --function-name cnDeleteFunction \
    --action lambda:InvokeFunction \
    --statement-id delete_func_statement_id-1 \
    --principal apigateway.amazonaws.com \
    --source-arn arn:aws:execute-api:$region:$account_id:$rest_api_id/*/DELETE/$resource_name

sleep 10
echo "Deploying the API"
aws apigateway create-deployment \
	--rest-api-id $rest_api_id \
        --stage-name production \
	--stage-description "Production stage"

sleep 5
aws apigateway update-stage --rest-api-id $rest_api_id \
    --stage-name production \
    --patch-operations op=replace,path=/*/*/logging/dataTrace,value=true

sleep 5
aws apigateway update-stage --rest-api-id $rest_api_id \
    --stage-name production \
    --patch-operations op=replace,path=/*/*/logging/loglevel,value=info