import sys
import boto3
import json

def transform_data(input_data):
    # Example transformation logic
    transformed_data = []
    for record in input_data:
        transformed_record = {
            'id': record['id'],
            'value': record['value'] * 2  # Example transformation
        }
        transformed_data.append(transformed_record)
    return transformed_data

def main():
    # Initialize a Glue context
    glue_context = boto3.client('glue')
    
    # Example: Fetch input data from a Glue table
    input_data = glue_context.get_table(DatabaseName='your_database', Name='your_table')['Table']['StorageDescriptor']['Columns']
    
    # Transform the data
    transformed_data = transform_data(input_data)
    
    # Output the transformed data (this could be saved to a database, S3, etc.)
    print(json.dumps(transformed_data))

if __name__ == "__main__":
    main()