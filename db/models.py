# -*- coding: utf-8 -*- 
'''
Created on 2015-9-1

@author: lsy
'''
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
SQLAlchemy models for warfare data.
"""
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Text
# from sqlalchemy import Text
# from sqlalchemy import Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.orm import object_mapper
# 
import datetime
import logging
# 
# from common import timeutils
# 
from scheduling.db.session import get_session
# from common.exception import DataBaseException as exception
# from common.config import config


LOG = logging.getLogger(__name__)

# FLAGS = flags.FLAGS
BASE = declarative_base()

def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.now()

utcnow.override_time = None

class SchedulingBase(object):
    """Base class for Warfare Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    id = Column(String(length=128), nullable=False, default=uuid.uuid1)
    created_at = Column(DateTime, default=utcnow())
    updated_at = Column(DateTime, onupdate=utcnow())
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def __init__(self):
        self._i = None

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        try:
            session.flush()
        except IntegrityError, e:
            if str(e).endswith('is not unique'):
                raise Exception.format(str(e))
            else:
                raise

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = utcnow()
        self.save(session=session)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()

    def dict(self):
        item_list = []
        for k,v in self.__dict__.iteritems():
            if not k[0] == '_' :
                if type(v) == datetime.datetime:
                    v=datetime.datetime.strftime(v,'%Y-%m-%d %H:%M:%S')
                item_list.append((k,v))

        joined = dict(item_list)
        return joined


class Staff(BASE, SchedulingBase):
    """Represents a staff
    """

    __tablename__ = 'staff'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1,primary_key=True)
    name = Column(String(length=255), nullable=False)
    role = Column(String(length=255), nullable=False)
    station = Column(String(length=255), nullable=False)

class BaseInfo(BASE, SchedulingBase):
    """Represents a base info
    """

    __tablename__ = 'base_info'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1,primary_key=True)
    station = Column(String(length=255), nullable=False)
    positions = Column(Text, nullable=False)
    jobs = Column(Text, nullable=False)
    association = Column(Text, nullable=True)
    weight_and_night = Column(Text, nullable=True)

class Scheduling(BASE, SchedulingBase):
    """Represents a scheduling
    """

    __tablename__ = 'scheduling'
    id = Column(String(length=128), nullable=False, default=uuid.uuid1,primary_key=True)
    base_info_id = Column(String(length=128), nullable=False)
    year = Column(String(length=255), nullable=False)
    month = Column(String(length=255), nullable=False)
    scheduling_list = Column(Text, nullable=True)
    merge_weight_dict = Column(Text, nullable=True)
    merge_night_job_num_dict = Column(Text, nullable=True)

if __name__=='__main__':
    import time
    print time.strftime('%Y-%m-%d',time.localtime(time.time()+3600*24*2))
