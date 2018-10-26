"""
Homework.
Task executor.
"""

import sys
import argparse
from functools import wraps
from pprint import pprint
import json
import jsonschema

#constant
TASK_EXEC_FUNCTION = 'function'
TASK_EXEC_BASE_CLASS = 'base_class'


class TaskException(Exception):
    """ base module exception """


class TaskExceptionWrongParameters(TaskException):
    """ An exception is thrown when the parameters for the task
        are incorrectly specified. """


class TaskExceptionWrongClassStruct(TaskException):
    """ An exception is thrown when the subclass for the task
        are incorrectly specified. """


class TaskStorage:
    """ Storage for task executors """
    tasks = {}

    @classmethod
    def add(cls, task_name, obj, type_obj, json_schema):
        """ add task executor to storage

            Attributes:
                task_name -- task name
                obj -- function or class
                type_obj -- type of obj
                json_schema -- task parameters json schema
        """
        if task_name is not None and type_obj in [TASK_EXEC_BASE_CLASS, TASK_EXEC_FUNCTION]:
            cls.tasks[task_name] = (obj, type_obj, json_schema)


    @classmethod
    def check_schema(cls, json_params, json_schema):
        """ validation of the specified task parameters

            Attributes:
                json_params -- task parameters in json
                json_schema -- json schema for check
        """
        try:
            jsonschema.validate(json_params, json_schema)
        except (jsonschema.exceptions.ValidationError,
                jsonschema.exceptions.SchemaError):
            return False
        return True


class BaseTask:
    """ base class for setting the task (for python 3.6) """
    name = None
    json_schema = None

    def __init_subclass__(cls):
        super().__init_subclass__()
        TaskStorage.add(cls.name, cls, TASK_EXEC_BASE_CLASS, cls.json_schema)

    def run(self, *args, **kwargs): #pylint: disable=W0613
        """ this method must be implemented """
        raise TaskExceptionWrongClassStruct(
            "Class '{0}': Method 'run' not implemented."
            .format(type(self).__name__))



class BaseTaskMeta(type):
    """ metaclass for registering a task defined by class
        (for python < 3.6 model)
    """
    name = None
    json_schema = None

    def __new__(cls, name, bases, dct):
        subcls = super(BaseTaskMeta, cls).__new__(cls, name, bases, dct)
        TaskStorage.add(subcls.name, subcls, TASK_EXEC_BASE_CLASS, subcls.json_schema)
        return subcls


class BaseTaskV2(metaclass=BaseTaskMeta):
    """ base class for setting the task (for python < 3.6) """

    def run(self, *args, **kwargs): #pylint: disable=W0613
        """ this method must be implemented """
        raise TaskExceptionWrongClassStruct(
            "Class '{0}': Method 'run' not implemented."
            .format(type(self).__name__))


def task(name, json_schema):
    """ decorator for registering a task defined by function """
    def decor(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            return func(*args, **kwargs)

        TaskStorage.add(name, wrap, TASK_EXEC_FUNCTION, json_schema)
        return wrap
    return decor


def get_cmd_args():
    """ get arguments from command line """
    parser = argparse.ArgumentParser(description='some task executor')
    parser.add_argument('task_name',
                        type=str,
                        help='task name')
    parser.add_argument('-p', '--params',
                        type=str,
                        required=True,
                        help='data for task in json')
    try:
        args = parser.parse_args()
        args.params = json.loads(args.params)
    except (json.JSONDecodeError, TypeError) as err:
        raise TaskExceptionWrongParameters("Wrong parameters: ", err)
    return args


def run_cli():
    """ perform a task using command line parameters """
    try:
        args = get_cmd_args()
        if args.task_name in TaskStorage.tasks.keys():
            task_executor, task_type, task_schema = TaskStorage.tasks[args.task_name]
            if TaskStorage.check_schema(args.params, task_schema):
                if task_type == TASK_EXEC_BASE_CLASS:
                    print(task_executor().run(**args.params))
                elif task_type == TASK_EXEC_FUNCTION:
                    print(task_executor(**args.params))
            else:
                print("parameters do not match the task '{0}'".format(args.task_name))
                pprint(task_schema)
        else:
            print("no task with that name: ", args.task_name)
    except TaskExceptionWrongParameters as err:
        print(err)
        print(sys.argv)


if __name__ == '__main__':
    run_cli()
