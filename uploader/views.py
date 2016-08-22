from __future__ import absolute_import
import os
from flask import request, render_template, session, flash, url_for, jsonify
from werkzeug.utils import secure_filename
from uploader import app
from .tasks import parse_csv
import requests

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main renderer"""

    if request.method == 'GET':
        return render_template('ind.html')

    if not 'file' in request.files:
        flash('No file part')
        return jsonify({}), 412

    if request.form['submit'] == 'Download':
        url = request.form.get('url', None)
        if not url:
            flash('No url provided')
            return jsonify({}), 412
        downloaded_file = requests.get(url)
        filename = secure_filename('default.csv')
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(save_path, 'wb') as f:
            f.write(downloaded_file.content)
        session['file_name'] = save_path

    else:
        file = request.files['file']
        if not file.filename:
            flash('No selected file')
            return jsonify({}), 412
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            session['file_name'] = save_path

    return jsonify({}), 202


@app.route('/parser', methods=['POST'])
def parser():
    task = parse_csv.apply_async(kwargs={"file_name": session.get('file_name', '')})
    if 'file_name' in session:
        del session['file_name']
    session['task_id'] = task.id
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    """Function which returns ;ast task, TODO: return "all tasks"""
    if 'task_id' in session:
        return jsonify(), 202, {'Task': url_for('taskstatus',
                                                task_id=session['task_id'])}
    else:
        return jsonify(), 412


@app.route('/status/<task_id>')
def taskstatus(task_id):
    """Status of Celery task"""
    task = parse_csv.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
