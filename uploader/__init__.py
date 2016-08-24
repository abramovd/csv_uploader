from flask import Flask
from celery import Celery
from flask.ext.sqlalchemy import SQLAlchemy
from config import UPLOAD_FOLDER, SQLALCHEMY_DATABASE_URI

ALLOWED_EXTENSIONS = {'jpg', 'csv'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],
                include=['uploader.tasks'])
celery.conf.update(app.config)

import views
import models
