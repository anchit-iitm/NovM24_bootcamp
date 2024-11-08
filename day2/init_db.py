# from app import app
# from flask import current_app as app
from app import create_app
from models import db, user_datastore

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user_datastore.find_or_create_role(name='admin', description='super user')

    # new_data = test(var1FromDb=var1, var2FromDb=var2, var3FromDb=var3)
    # db.session.add(new_data)
    user_datastore.find_or_create_role(name='manager', description='middle level user')
    user_datastore.find_or_create_role(name='customer', description='lower level user')
    db.session.commit()

    admin_user = user_datastore.find_user(email='a@a.com')
    if not admin_user:
        new_user = user_datastore.create_user(email='a@a.com', password='a')
        user_datastore.add_role_to_user(new_user, 'admin')
        db.session.commit()

    manager_user = user_datastore.find_user(email='m@a.com')
    if not manager_user:
        new_user = user_datastore.create_user(email='m@a.com', password='m')
        user_datastore.add_role_to_user(new_user, 'manager')
        db.session.commit()
    
    customer_user = user_datastore.find_user(email='c@a.com')
    if not customer_user:
        new_user = user_datastore.create_user(email='c@a.com', password='c')
        user_datastore.add_role_to_user(new_user, 'customer')
        db.session.commit()
