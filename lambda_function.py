mport json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('StreamGuardSubscriptions')

def lambda_handler(event, context):
    sub_id = str(event.get('subscription_id', '')).strip().upper()

    if not sub_id:
        return {"decision": "DENIED", "reason": "Missing subscription_id parameter."}

    try:
        response = table.get_item(Key={'subscription_id': sub_id})
        item = response.get('Item')

        if not item:
            return {"decision": "DENIED", "reason": f"Subscription {sub_id} not found."}
        
        if item.get('account_flag') != 'CLEAN':
            return {
                "decision": "DENIED", 
                "reason": "Account flagged for previous chargeback/fraud risk. Automatic refund blocked."
            }
        
        if float(item.get('plan_amount', 0)) > 50.00:
            return {
                "decision": "ESCALATE_TO_HUMAN", 
                "reason": f"Amount (${item['plan_amount']}) exceeds the $50.00 automated limit. Escalated to human review."
            }
        
        if int(item.get('watch_percentage', 100)) > 10:
            return {
                "decision": "DENIED", 
                "reason": f"Usage is {item['watch_percentage']}%, exceeding the 10% refund policy limit."
            }
        
        if item.get('status') != 'ACTIVE':
            return {
                "decision": "DENIED", 
                "reason": f"Subscription status is {item['status']}, not eligible for refund."
            }
        
        table.update_item(
            Key={'subscription_id': sub_id},
            UpdateExpression="set #st = :r",
            ExpressionAttributeNames={'#st': 'status'},
            ExpressionAttributeValues={':r': 'REFUNDED'}
        )
        return {
            "decision": "APPROVED", 
            "reason": f"Refund of ${item['plan_amount']} approved for {item['user_name']} ({sub_id})."
        }
            
    except Exception as e:
        return {"decision": "ERROR", "reason": str(e)}



