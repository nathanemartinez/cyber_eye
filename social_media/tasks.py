# from huey import SqliteHuey
from huey.contrib.djhuey import task
from social_media.models.twitter_model import DummyModel
# huey = SqliteHuey(filename='db.sqlite3')

# @settings.HUEY.task()
@task()
def add(num, id):
	obj = DummyModel.objects.get(id=id)
	obj.integer += num
	obj.save()
