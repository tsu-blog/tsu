import os
import json

def handler(event, context):
    # TODO implement
    env_var_dict = {
        'time': os.environ['TZ'],
        'exec_env': os.environ['AWS_EXECUTION_ENV'],
        'task': os.environ['LAMBDA_TASK_ROOT'],
        'runtime_dir': os.environ['LAMBDA_RUNTIME_DIR'],
        'region': os.environ['AWS_REGION'],
        'default_region': os.environ['AWS_DEFAULT_REGION'],
        'log_group': os.environ['AWS_LAMBDA_LOG_GROUP_NAME'],
        'log_stream': os.environ['AWS_LAMBDA_LOG_STREAM_NAME'],
        'function_name': os.environ['AWS_LAMBDA_FUNCTION_NAME'],
        'function_memory_size': os.environ['AWS_LAMBDA_FUNCTION_MEMORY_SIZE'],
        'function_version': os.environ['AWS_LAMBDA_FUNCTION_VERSION'],
        'path': os.environ['PATH'],
        'ld_library_path': os.environ['LD_LIBRARY_PATH'],
        #'node_path': os.environ['NODE_PATH'],
        'python_path': os.environ['PYTHONPATH'],
        'lang': os.environ['LANG']
    }

    return {
        "statusCode": 200,
        "body": json.dumps(env_var_dict)
    }
