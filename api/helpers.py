
import importlib

def call_method_from_string(method_string, payload = None):
    '''
    given a string path, call the method
    '''
    parts = method_string.split('.') # qualified method: e.g.: api.tasks.ping
    method_to_call = parts.pop()
    module_string = ('.').join(parts)
    module = importlib.import_module(module_string)
    func = getattr(module, method_to_call)
    return func(payload)

def get_tasks_by_module_string(module_string):
    module = importlib.import_module(module_string)
    tasks = []
    for method_string in dir(module):
        method = getattr(module, method_string)
        if callable(method):
            tasks.append({
                "name": method_string,
                "docs": method.__doc__
            })
    return tasks