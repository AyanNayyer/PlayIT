from flask import Flask
from flask_security import Security
from models import db
from api_resources import api
from databasefile import datastore
import secrets
from worker import celery_init_app
from sample_data import initialize_sample_data
import flask_excel as excel
from celery.schedules import crontab
from tasks import monthly_reminder, daily_reminder
from cache import cache
from mail import mail
from flask_mail import Mail
from mailconfig import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD

###app instance

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdb.sqlite3'
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SECURITY_PASSWORD_SALT'] = 'randomizedsecrettoken4541'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_KEY_PREFIX'] = 'my_prefix'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 4
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['CACHE_REDIS_DEBUG'] = True
    cache.init_app(app)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    
    mail=Mail(app)
    mail.init_app(app)
    with app.app_context():
        mail.connect()
    
    with app.app_context():
        import controller
        
    
    return app

app = create_app()



### Celery App instance
celery_app = celery_init_app(app)



@celery_app.on_after_configure.connect
def celery_job(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=8, minute=0, day_of_month=1), monthly_reminder.s())
    # sender.add_periodic_task(crontab(hour=18, minute=0), daily_reminder.s())

    # for testing
    sender.add_periodic_task(20, monthly_reminder.s())
    sender.add_periodic_task(60, daily_reminder.s())



if __name__ == '__main__':
    initialize_sample_data()
    app.run(debug=True)
