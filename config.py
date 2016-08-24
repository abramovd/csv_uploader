import os
basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, 'media')

SQLALCHEMY_MIGRATE_REPO = 'migrations'
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/categ'
