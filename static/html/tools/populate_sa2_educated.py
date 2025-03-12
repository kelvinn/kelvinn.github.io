__author__ = 'kelvinn'
from sqlalchemy import *
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy import postgis
from geoalchemy import *
import simplejson as json
import urllib2
import os
import csv
import itertools

#Create and engine and get the metadata
#Base = declarative_base()

engine = create_engine('postgresql://abs:abs@192.168.70.128/', echo=False) #change here if want to view echo
Session = sessionmaker(bind=engine)
session = Session()


metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)

meta_reflected = MetaData(bind=engine, reflect=True)

class sydney_educated(Base):
    __tablename__ = 'sydney_educated'
    __table_args__ = {'autoload': True}
    geom = GeometryColumn(MultiPolygon(1,srid=4326))

edu_dict = {}

with open('educated.csv', 'rb') as csvfile:
    edureader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in edureader:
        edu_dict[row[0]] = row[1:]

sa2_list = session.query(sydney_educated).all()
for sa2_obj in sa2_list:
    try:
#        educated_percent = int(edu_dict[sa2_obj.sa2_name11][2] * 100)

        sa2_obj.total_persons = edu_dict[sa2_obj.sa2_name11][0]
        sa2_obj.total_educated = edu_dict[sa2_obj.sa2_name11][1]
        sa2_obj.educated_percent = edu_dict[sa2_obj.sa2_name11][2]
        session.add(sa2_obj)
        print edu_dict[sa2_obj.sa2_name11]

    except:
        pass

session.commit()

"""
  total_persons numeric,
  total_educated numeric,
  educated_percent numeric,
"""

"""
mb_list = session.query(mb_2011_nsw).filter(mb_2011_nsw.gcc_code11 == '1GSYD').all()
for mb_obj in mb_list:
    try:
        mb_obj.commute_time = location_dict[mb_obj.mb_code11][1]
        mb_obj.commute_dest = location_dict[mb_obj.mb_code11][0]
        session.add(mb_obj)
    except:
        print "Failed to look up mb_obj in location_dict", mb_obj.mb_code11
session.commit()
"""