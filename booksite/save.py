import django
django.setup()
import datetime

from django.contrib.auth.models import User
from accounts.models import UserProfile
import sqlite3
syan = User.objects.all().first()
profile = UserProfile.objects.get(user=syan)
profile.company = 'hah'
profile.birth = datetime.date(1997,2,1)
try:
    import pdb;pdb.set_trace();
    profile.save()
except django.db.utils.IntegrityError:
    from django.db import connection
    queries = connection.queries
    for query in queries:
        print(query)