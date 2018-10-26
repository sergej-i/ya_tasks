# file: my_tasks.py
from ya_tasks import tasks
from functools import reduce


@tasks.task(name='multiprint', 
            json_schema={'type': 'object',
                         'properties': {
                            'msg': {'type': 'string'},
                            'count': {'type': 'integer', 'minimum': 1}
                            },
                            'required': ['msg']})
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in range(count))


#class Multiply(tasks.BaseTaskV2):
class Multiply(tasks.BaseTask):
    name = 'mult'
    json_schema = {'type': 'object',
                   'properties': {
                       'operands': {'type': 'array',
                                    'minItems': 1,
                                    'items': {'type': 'number'}}
                    },
                    'required': ['operands']}
    def run(self, operands):
        return reduce(lambda x, y: x*y, operands)


if __name__ == '__main__':
    tasks.run_cli()
