import json
import os
from faker import Faker
from jobplus.models import db, User, Company

f = Faker(locale='zh-cn')

def iter_companies():
    with open(os.path.join(os.path.dirname(__file__),'..','datas','companies.json')) as f:
        companies = json.load(f)
    for company in companies:
            yield User(
                    name=company['name'],
                    email=f.email(),
                    password=f.password(),
                    role=User.ROLE_COMAPNY,
                    
                    )
            
def iter_companies_msg():
    with open(os).path.join(os.path.dirname(__file__),'..','datas','companies.json') as f:
        companies_msg = json.load(f)
    for company_msg in companies_msg:
        user = User.query.filter_by(name=company_msg['name']).first()
        yield company_msg(
                logo=company_msg['logo'],
                user=user,
                address=f.address(),
                oneword_profile=f.sentence(),
                detail=f.text(),
                website=f.url(),
                slug=Faker().word()
                )
            
def run():
    for company in iter_companies():
        db.session.add(company)
                
    for company_msg in iter_companies_msg():
        db.session.add(company_msg)

    try:
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()



