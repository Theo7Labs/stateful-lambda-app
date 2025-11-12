import json
import os
import boto3

# 1. Get the table name from an environment variable
TABLE_NAME = os.environ.get('STATE_TABLE_NAME')

# 2. Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    This function increments a visit counter in a DynamoDB table.
    """
    
    session_id = "user_123"
    
    try:
        # 4. Try to get the item (the row) from the table
        response = table.get_item(
            Key={'session_id': session_id}
        )
        
        # 5. Check if the user has visited before
        if 'Item' in response:
            # If "Item" exists, they have visited. Get the count.
            visit_count = response['Item']['visit_count']
            
            # --- THIS IS THE FIX ---
            # Convert the "Decimal" number from DynamoDB into a simple integer
            visit_count = int(visit_count) 
            
            visit_count = visit_count + 1
            message = "Welcome back! This is your " + str(visit_count) + " visit."
        else:
            # If no "Item", this is their first visit.
            visit_count = 1
            message = "Welcome! This is your first visit."

        # 6. Write the new count back to the database
        table.put_item(
            Item={
                'session_id': session_id,
                'visit_count': visit_count
            }
        )

        # 7. Return a successful message
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": message,
                "session_id": session_id,
                "visit_count": visit_count
            }),
        }

    except Exception as e:
        # Handle any errors
        print(f"Error: {e}") # This prints the REAL error to CloudWatch
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error interacting with the database."
            }),
        }