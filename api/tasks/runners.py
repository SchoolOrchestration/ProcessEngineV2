'''
Various runners for performing tasks
'''
import requests
from ..helpers import call_method_from_string

def http_task_runner(task):
    url = "http://{}/tasks/".format(task.service)
    data = {
        "task": task.method_name,
        "payload": task.payload
    }
    result = requests.post(url, json=data)
    success = result.status_code < 300
    return (result, success)

def call(runner, task):
    return call_method_from_string(runner, task)
