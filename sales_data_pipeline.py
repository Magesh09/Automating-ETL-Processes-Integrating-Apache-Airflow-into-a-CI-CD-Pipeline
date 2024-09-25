import boto3
import pandas as pd
import csv

def extract_data():
    s3 = boto3.client('s3')
    s3.download_file('my-sales-bucket', 'sales_data.csv', '/tmp/sales_data.csv')

def transform_data():
    df = pd.read_csv('/tmp/sales_data.csv')
    df['TotalAmount'] = df['Quantity'] * df['Price']
    df.to_csv('/tmp/transformed_sales_data.csv', index=False)

def load_data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SalesData')

    with open('/tmp/transformed_sales_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table.put_item(Item={
                'OrderID': row['OrderID'],
                'TotalAmount': row['TotalAmount']
            })

def send_notification():
    sns = boto3.client('sns')
    sns.publish(TopicArn='arn:aws:sns:us-west-2:123456789012:SalesDataNotification', Message='Sales data processed!')

if __name__ == "__main__":
    extract_data()
    transform_data()
    load_data()
    send_notification()