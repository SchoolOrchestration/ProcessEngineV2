'''
A collection of generally useful tasks
Call with: tasks.runner
'''

def make_http_request(payload):
    """
    Make an HTTP request:

    **e.g.:**
    ```
    result = make_http_request({
        "url": url,
        "data": data,
        "method": "post",
        "heders": headers,
    })
    ```
    """
    pass

def slack_message(payload):
    pass

def ping(payload):
    return {"message": "pong"}