db = db.getSiblingDB('caelus');
db.createCollection('USERS');

db.USERS.insertOne({
    'username':'admin',
    'password':'$2b$12$SOKE1KeCVE5/rR/uM3RN4ujJsosxyZnstsEnTnEBgXroqME1reSr6'
});

