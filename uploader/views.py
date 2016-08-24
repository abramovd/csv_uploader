from __future__ import absolute_import
import os
from flask import request, render_template, session, flash, url_for, jsonify
from werkzeug.utils import secure_filename
from uploader import app
from .tasks import parse_csv
import requests
import shortuuid


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def safe_filename(filename):
    if not os.path.isfile(filename):
        return filename
    dir_name, file_name = os.path.split(filename)
    file_root, file_ext = os.path.splitext(file_name)
    uuid = shortuuid.uuid()
    filename = secure_filename('{0}_{1}{2}'.format(
                               file_root,
                               uuid,
                               file_ext))

    return filename


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main renderer"""

    if request.method == 'GET':
        return render_template('index.html')

    if request.form.get('submit', None) == 'Download':
        url = request.form.get('url', None)
        if not url:
            return jsonify({'error': 'No url provided'}), 412
        elif url[-3:] != 'csv':
            return jsonify({'error': 'No csv file'}), 412

        try:
            downloaded_file = requests.get(url)
        except requests.exceptions.RequestException:
            return jsonify({'error': 'cannot download by url'}), 412

        filename = safe_filename(os.path.join(app.config['UPLOAD_FOLDER'],
                                              'default.csv'))
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(save_path, 'wb') as f:
            f.write(downloaded_file.content)
        session['filename'] = save_path

    else:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 412

        file = request.files['file']
        if not file.filename:
            return jsonify({'error': 'No selected file'}), 412
        if file and allowed_file(file.filename):
            filename = safe_filename(os.path.join(app.config['UPLOAD_FOLDER'],
                                                  file.filename))
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            session['filename'] = save_path
        else:
            return jsonify({'error': 'bad extension'}), 412

    return jsonify(), 202


@app.route('/parser', methods=['POST'])
def parser():
    if 'filename' not in session:
        return jsonify({}), 412
    task = parse_csv.apply_async(kwargs={"filename":
                                         session.get('filename')})
    if 'filename' in session:
        del session['filename']
    session['task_id'] = task.id
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    """Function which returns last task, TODO: return "all tasks"""
    if 'task_id' in session:
        return jsonify(), 202, {'Task': url_for('taskstatus',
                                                task_id=session['task_id'])}
    else:
        return jsonify(), 412


@app.route('/status/<task_id>')
def taskstatus(task_id):
    """Status of Celery task"""
    task = parse_csv.AsyncResult(task_id)

    response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }

    if task.state == 'PENDING':
        response.update(current=0, total=1, status='Pending...')

    elif task.state != 'FAILURE':
        response.update(current=task.info.get('current', 0),
                        total=task.info.get('total', 1),
                        status=task.info.get('status', '')
                        )
        if 'result' in task.info:
            response.update(result=task.info['result'])

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
