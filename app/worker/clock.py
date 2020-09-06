"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
import random
import string

from flask_bcrypt import generate_password_hash
from apscheduler.schedulers.background import BackgroundScheduler

from app import db
from app.models.user import User

def tick():
    hashed_password = generate_password_hash('test_password').decode('utf-8')
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    user = User(
            firstname='Random',
            lastname='Test',
            email=f"{result_str@test.com",
            password=hashed_password
            )
    db.session.add(user)
    db.session.commit()
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
