import json
import boto3

# import requests


def listcluster():
    client = boto3.client('ecs')
    response = client.list_clusters()
    return response['clusterArns']


def listtasks(cluster_name):
    client = boto3.client('ecs')
    response = client.list_tasks(cluster=cluster_name)
    return response['taskArns']


def stop_tasks(cluster_name, task_name):
    client = boto3.client('ecs')
    response = client.stop_task(cluster=cluster_name, task=task_name, reason='programmatically stopping')
    return "success"


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    return_value = ""
    if event['request_type'] == 'clusterlist':
        all_clusters = listcluster()
        string_clusters = ""
        for single_cluster in all_clusters:
            if string_clusters == "":
                string_clusters = single_cluster
            else:
                string_clusters = string_clusters + "," + single_cluster
        return_value = string_clusters
    if event['request_type'] == 'tasklist':
        cluster_name = event['cluster_name']
        task_list = listtasks(cluster_name)
        string_tasks = ""
        for single_task in task_list:
            if string_tasks == "":
                string_tasks = single_task
            else:
                string_tasks = string_tasks + "," + single_task
        return_value = string_tasks
    if event['request_type'] == 'stoptask':
        cluster_name = event['cluster_name']
        task_name = event['task_name']
        return_value = stop_tasks(cluster_name, task_name)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": return_value,
            # "location": ip.text.replace("\n", "")
        })
    }
