# -*- coding: utf-8 -*-
'''
Created on 2015-9-1

@author: lsy
'''
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql.base import MEDIUMTEXT
from sqlalchemy import Table,Column,Integer,String,Boolean,DateTime,Text,LargeBinary,DECIMAL


engine = create_engine('mysql://root:123456@120.77.32.224:3306/jindou_system?charset=utf8',echo=False)
metadata = MetaData(engine)
table_list = []

# 创建数据库表
staff_table=Table('staff',metadata,
                    Column('id',String(128),primary_key=True),
                    Column('name',String(255),nullable=False),
                    Column('role',String(255), nullable=False),
                    Column('station',String(255), nullable=False),
                    Column('created_at',DateTime(timezone=False)),
                    Column('updated_at',DateTime(timezone=False)),
                    Column('deleted_at',DateTime(timezone=False)),
                    Column('deleted',Boolean(create_constraint=True, name=None))
                 )
table_list.append(staff_table)

base_info_table=Table('base_info',metadata,
                    Column('id',String(128),primary_key=True),
                    Column('station',String(length=255), nullable=False),
                    Column('positions',Text, nullable=False),
                    Column('jobs',Text, nullable=False),
                    Column('association',Text, nullable=True),
                    Column('weight_and_night',Text, nullable=True),
                    Column('created_at',DateTime(timezone=False)),
                    Column('updated_at',DateTime(timezone=False)),
                    Column('deleted_at',DateTime(timezone=False)),
                    Column('deleted',Boolean(create_constraint=True, name=None))
                 )
table_list.append(base_info_table)

scheduling_table=Table('scheduling',metadata,
                    Column('id',String(128),primary_key=True),
                    Column('base_info_id',String(128), nullable=False),
                    Column('year',String(length=255), nullable=False),
                    Column('month',String(length=255), nullable=False),
                    Column('scheduling_list',Text, nullable=False),
                    Column('merge_weight_dict',Text, nullable=False),
                    Column('merge_night_job_num_dict',Text, nullable=False),
                    Column('created_at',DateTime(timezone=False)),
                    Column('updated_at',DateTime(timezone=False)),
                    Column('deleted_at',DateTime(timezone=False)),
                    Column('deleted',Boolean(create_constraint=True, name=None))
                 )
table_list.append(scheduling_table)

# #删除所有表
# for table in table_list:
#     try:
#         table.drop()
#         print "Drop Table %s Success !"%table.fullname
#     except Exception,e:
#         print e.message

#创建所有表
for table in table_list:
    try:
        table.create()
        print "Create Table %s Success !"%table.fullname
    except Exception,e:
        print e.message


# #创建单个表
# application_table.create()