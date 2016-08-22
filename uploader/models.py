from __future__ import absolute_import
from uploader import db


class CategoryLine(db.Model):
    __tablename__ = 'categori'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    real_category_id = db.Column(db.Integer)
    categories_id_lvl0 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl1 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl2 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl3 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl4 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl5 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl6 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl7 = db.Column(db.String(1000), nullable=True)
    categories_id_lvl8 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl0 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl1 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl2 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl3 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl4 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl5 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl6 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl7 = db.Column(db.String(1000), nullable=True)
    categories_name_lvl8 = db.Column(db.String(1000), nullable=True)