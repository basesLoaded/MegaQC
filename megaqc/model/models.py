# -*- coding: utf-8 -*-
import datetime as dt

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, ForeignKey, Column, Boolean, Integer, Float, String, TIMESTAMP, Binary, DateTime, func

from megaqc.database import CRUDMixin
from megaqc.extensions import db

class Report(db.Model, CRUDMixin):
    """a MultiQC report"""

    __tablename__ = 'report'
    report_id = Column(Integer, primary_key=True)
    report_hash = Column(String)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(Report.report_id)).first()[0] or 0) + 1

    def __init__(self, **kwargs):
        """Create instance."""
        if "report_id" not in kwargs:
            kwargs['report_id'] = Report.get_next_id()
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Report({title!r})>'.format(title=self.title)




class ReportMeta(db.Model, CRUDMixin):
    __tablename__ =  'report_meta'
    report_meta_id = Column(Integer, primary_key=True)
    report_meta_key = Column(String(80), nullable=False)
    report_meta_value = Column(String(80), nullable=False)
    report_id = Column(Integer, ForeignKey('report.report_id'))

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(ReportMeta.report_meta_id)).first()[0] or 0) + 1

class  PlotConfig(db.Model, CRUDMixin):
    __tablename__ =  'plot_config'
    config_id = Column(Integer, primary_key=True)
    config_type = Column(String(80),  nullable=False)
    config_name = Column(String(80), nullable=False)
    config_dataset = Column(String(80), nullable=True)
    data = Column(String(2048), nullable=False)

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(PlotConfig.config_id)).first()[0] or 0) + 1

class PlotData(db.Model, CRUDMixin):
    __tablename__ = "plot_data"
    plot_data_id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('report.report_id'))
    config_id = Column(Integer, ForeignKey('plot_config.config_id'))
    plot_category_id = Column(Integer(), ForeignKey('plot_category.plot_category_id'))
    sample_id = Column(Integer, ForeignKey('sample.sample_id'))
    data = Column(String(2048), nullable=False)

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(PlotData.plot_data_id)).first()[0] or 0) + 1

class PlotCategory(db.Model, CRUDMixin):
    __tablename__ = "plot_category"
    plot_category_id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('report.report_id'))
    config_id = Column(Integer, ForeignKey('plot_config.config_id'))
    category_name = Column(String(120), nullable=True)
    data = Column(String(2048), nullable=False)

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(PlotCategory.plot_category_id)).first()[0] or 0) + 1

class SampleDataType(db.Model, CRUDMixin):
    __tablename__ = "sample_data_type"
    sample_data_type_id = Column(Integer, primary_key=True)
    data_id = Column(Integer)
    data_section = Column(String(80))
    data_key = Column(String(80), nullable=False)

class SampleData(db.Model, CRUDMixin):
    __tablename__ = "sample_data"
    sample_data_id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('report.report_id'))
    sample_data_type_id = Column(Integer, ForeignKey('sample_data_type.sample_data_type_id'))
    sample_id = Column(Integer, ForeignKey('sample.sample_id'))
    value = Column(String(80))

    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(SampleData.sample_data_id)).first()[0] or 0) + 1


class Sample(db.Model, CRUDMixin):
    __tablename__ ="sample"
    sample_id=Column(Integer, primary_key=True)
    sample_name=sample_name = Column(String(80)) 
    report_id = Column(Integer, ForeignKey('report.report_id'))
    @staticmethod
    def get_next_id():
        return (db.session.query(func.max(Sample.sample_id)).first()[0] or 0) + 1
