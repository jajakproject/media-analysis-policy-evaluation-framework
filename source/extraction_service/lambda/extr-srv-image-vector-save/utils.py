import boto3
import numbers,decimal
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource('dynamodb')

def dynamodb_table_upsert(table_name, document):
    try:
        document = convert_to_dynamo_format(document)
        video_task_table = dynamodb.Table(table_name)
        return video_task_table.put_item(Item=document)
    except Exception as e:
        print(f"An error occurred, dynamodb_table_upsert: {e}")
        return None
    
def dynamodb_get_by_id(table_name, id, key_name="Id"):
    try:
        video_task_table = dynamodb.Table(table_name)
        response = video_task_table.get_item(Key={key_name: id})
        if 'Item' in response:
            return convert_decimal_to_float(response['Item'])
        else:
            print(f"No item found with id: {id}")
            return None
    except Exception as e:
        print(f"An error occurred, dynamodb_get_by_id: {e}")
        return None
    return None

def convert_to_dynamo_format(item):
    """
    Recursively convert a DynamoDB item to a JSON serializable format.
    """
    if isinstance(item, dict):
        return {k: convert_to_dynamo_format(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [convert_to_dynamo_format(v) for v in item]
    elif isinstance(item, float):
        return decimal.Decimal(str(item))
    #elif isinstance(item, decimal.Decimal):
    #    return float(item)
    else:
        return item


def convert_decimal_to_float(obj):
    if isinstance(obj, list):
        return [convert_decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
