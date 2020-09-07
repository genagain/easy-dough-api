from datetime import datetime

from app import create_app, scheduler
from app.models.user import User

app = create_app()

def tick():
    print('Tick! The time is: %s' % datetime.now())
    with app.app_context():
        print(User.query.all())

scheduler.add_job(tick, 'interval', seconds=10)
scheduler.start()
