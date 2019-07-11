from client.client_log_config import *


functions = []
log_msgs = []

def decolog(function):
    functions.append(function.__name__)

    if len(functions) > 1:
        for num_func, func in enumerate(functions):
            if func == function.__name__:
                parent_func = functions[num_func-1]
                client_log.info(f'Function {func} called from {parent_func}')
    else:
        func = function.__name__
        client_log.info(f'Function {func} havent parent function')

    return function
