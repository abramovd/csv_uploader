from __future__ import absolute_import
import os
from uploader import db, celery, UPLOAD_FOLDER
from .models import CategoryLine
import pandas as pd


def load_data(file_name):
    return pd.read_csv(os.path.join(UPLOAD_FOLDER, file_name), sep='\t')


@celery.task(bind=True, name='parse_csv')
def parse_csv(self, file_name=''):
    """Background task that parses CSV file"""
    try:
        data = load_data(file_name)
    except IOError:
        return {'current': 0, 'total': 100, 'status': 'Cannot read file',
                'result': 42}

    total = len(data)
    for ind, row in data.iterrows():
        self.update_state(state='PROGRESS',
                          meta={'current': ind + 1, 'total': total,
                                'status': 'Parsing'})
        record = CategoryLine(**row.to_dict())
        db.session.add(record)
        db.session.commit()
    return {'current': 100, 'total': 100, 'status': 'Parsed!'}