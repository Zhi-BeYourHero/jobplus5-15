import json, os, sys
from faker import Faker
sys.path.append('/home/zhi/jobplus5-15/jobplus')
from models import db, User, Job

f = Faker(locale='zh-cn')

def iter_jobs_msg():
    with open(os.path.join(os.path.dirname(__file__),'..','datas','jobsmsg.json')) as ff:
        jobs = json.load(ff)
    for job in jobs:
        yield Job(
            name=job['name'],
            degree_requirement=job['degree_requirement'],
            experience_requirement=job['experience_requirement'],
            salary=job['salary'],
            address=job['address'],
            tags=job['tags'],
            company=User.query.filter_by(name=job['company']).first()
        )

def run():
    for job in iter_jobs_msg():
        db.session.add(job)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

