from flask import Flask, render_template
from task_pipeline.pipeline import Pipeline
from user import create_new_user
import json
app = Flask(__name__)


@app.route('/')
def index():
    return "hello"


all_users = {}


@app.route("/create/<name>")
def create_user(name):
    user = create_new_user(name)
    all_users[name] = user
    return json.dumps(all_users[name].__dict__)


@app.route("/user/<name>")
def get_user(name):
    if name in all_users:
        user = json.dumps(all_users[name].__dict__)
        return user
    else:
        return "fail"


all_pipelines = {}


@app.route("/create_pipe")
def create_pipeline():
    task = None
    stage_group = None

    pipeline = Pipeline(task, stage_group)
    all_pipelines[pipeline.id] = pipeline


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
