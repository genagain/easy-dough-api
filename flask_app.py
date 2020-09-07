from datetime import datetime

from app import create_app
from app import scheduler
app = create_app()

def tick():
    print('Tick! The time is: %s' % datetime.now())
    with app.app_context():
        from app.models.user import User
        print(User.query.all())

scheduler.add_job(tick, 'interval', seconds=10)
scheduler.start()
