import boto3

def lambda_handler(value, context):

   connector = boto3.resource('dynamodb')

   db = connector.Table('cnTable')
   
   api_resp = db.put_item(

   Item={
   "id": value['id'],

   "City": value['City'],

   "Model": value['Model'],

   "Output": value['Output'],

   "PostCode": value['PostCode'],

   "SN": value['SN'],
           
   "Street": value['Street']

   }

   )
   return {
   'statusCode': api_resp['ResponseMetadata']['HTTPStatusCode'],

   'API response': 'Record ' + value['id'] + ' added'

}
