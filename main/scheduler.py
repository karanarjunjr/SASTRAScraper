from apscheduler.schedulers.background import BackgroundScheduler
from . import views

        
def start():
        scheduler = BackgroundScheduler()
        scheduler.add_job(views.sendEmail, 'interval', minutes=60)
        scheduler.start()
    