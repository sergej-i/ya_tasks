from flask import Flask, render_template, request
import json
import tasks
import tasks_description

app = Flask(__name__)

@app.route('/')
def hello() -> 'html':
    return render_template('index.html', the_title = 'hello ya_task')

@app.route('/form')
def form_page() -> 'html':
    return render_template('form.html', the_title = 'hello ya_task')

@app.route('/result', methods=['POST'])
def result_page() -> str:
    task_name = request.form['task_name']
    params = json.loads(request.form['params']) # TODO check json

    if task_name in tasks.TaskStorage.tasks.keys():
        task_executor, task_type, task_schema = tasks.TaskStorage.tasks[task_name]
        if tasks.TaskStorage.check_schema(params, task_schema):
            if task_type == tasks.TASK_EXEC_BASE_CLASS:
                return str(task_executor().run(**params))
            elif task_type == tasks.TASK_EXEC_FUNCTION:
                return str(task_executor(**params))
        else:
            return "parameters do not match the task '{0}' ({1})".format(task_name, params)
    else:
        return "no task with that name: {0}".format(task_name)

    return str(request.form)


app.run(host='0.0.0.0', port=8000, debug=True)
