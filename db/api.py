# -*- coding: utf-8 -*- 
'''
Created on 2015-9-1

@author: lsy
'''
#encoding: utf-8
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

"""Implementation of SQLAlchemy backend."""

import logging
import datetime
from scheduling.db.session import get_session
from scheduling.db import models



# FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)



def model_query( *args, **kwargs):
    """Query helper that accounts for 's `read_deleted` field.

    :param :  to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides 's read_deleted field.
    :param project_only: if present and  is user-type, then restrict
            query to match the 's project_id.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or 'no'

    query = session.query(*args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
            "Unrecognized read_deleted value '%s'") % read_deleted


    return query


###################
_ISO8601_TIME_FORMAT_SUBSECOND = '%Y-%m-%dT%H:%M:%S.%f'
PERFECT_TIME_FORMAT = _ISO8601_TIME_FORMAT_SUBSECOND
 
def parse_strtime(timestr, fmt=PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(timestr, fmt)
 
def convert_datetimes(values, *datetime_keys):
    for key in values:
        if key in datetime_keys and isinstance(values[key], basestring):
            values[key] = parse_strtime(values[key])
    return values


def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.now()

utcnow.override_time = None



#######staff表操作
def staff_create( values, session=None):
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        staff_ref = models.Staff()
        session.add(staff_ref)
        staff_ref.update(values)
    return staff_ref

def staff_get_all( session=None):
    return model_query(models.Staff, session=session).\
            order_by(models.Staff.station.desc()).\
            order_by(models.Staff.role.desc()).\
            all()

def staff_get_by_id(staff_id,session=None):
    return model_query(models.Staff, session=session).\
            filter_by(id=staff_id).\
            first()

def staff_get_by_role_and_station(role,station,session=None):
    return model_query(models.Staff, session=session).\
            filter_by(role=role).\
            filter_by(station=station).\
            all()

def staff_destroy(staff_id):
    session = get_session()
    with session.begin(subtransactions=True):
        session.query(models.Staff).filter_by(id=staff_id).delete()
        session.flush()
        return True

def staff_get_count_by_role_and_station(role,station,session=None):
    query = model_query(models.Staff, session=session).\
            filter_by(role=role).\
            filter_by(station=station).\
            count()
    return query

#######base_info表操作
def base_info_create( values, session=None):
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        base_info_ref = models.BaseInfo()
        session.add(base_info_ref)
        base_info_ref.update(values)
    return base_info_ref

def base_info_get_by_id(base_info_id, session=None):
    result = model_query(models.BaseInfo, session=session).\
                        filter_by(id=base_info_id).first()
    return result

def base_info_update_by_id( base_info_id, values):
    session = get_session()

    with session.begin(subtransactions=True):
        values['updated_at'] = utcnow()
        convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
        base_info_ref = base_info_get_by_id( base_info_id, session=session)

        for (key, value) in values.iteritems():
            base_info_ref[key] = value
        base_info_ref.save(session=session)
        return base_info_ref

def base_info_get_all( session=None):
    return model_query(models.BaseInfo, session=session).\
            all()

def base_info_destroy(base_info_id):
    session = get_session()
    with session.begin(subtransactions=True):
        session.query(models.BaseInfo).filter_by(id=base_info_id).delete()
        session.flush()
        return True

#######scheduling表操作
def scheduling_create( values, session=None):
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        scheduling_ref = models.Scheduling()
        session.add(scheduling_ref)
        scheduling_ref.update(values)
    return scheduling_ref

def scheduling_get_by(base_info_id,year,month,session=None):
    result = model_query(models.Scheduling, session=session).\
                        filter_by(base_info_id=base_info_id).\
                        filter_by(year=year).\
                        filter_by(month=month).\
                        first()
    return result

def scheduling_get_by_id(scheduling_id, session=None):
    result = model_query(models.Scheduling, session=session).\
                        filter_by(id=scheduling_id).first()
    return result

def scheduling_update_by_id(scheduling_id, values):
    session = get_session()

    with session.begin(subtransactions=True):
        values['updated_at'] = utcnow()
        convert_datetimes(values, 'created_at', 'deleted_at', 'updated_at')
        scheduling_ref = scheduling_get_by_id( scheduling_id, session=session)

        for (key, value) in values.iteritems():
            scheduling_ref[key] = value
        scheduling_ref.save(session=session)
        return scheduling_ref

def scheduling_get_all( session=None):
    return model_query(models.Scheduling, session=session).\
            all()

if __name__=='__main__':
    pass