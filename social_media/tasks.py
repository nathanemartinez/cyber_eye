# # from huey import SqliteHuey
# from huey.contrib.djhuey import task
# from django.conf import settings
# from social_media.models.twitter_model import DummyModel
# # huey = SqliteHuey(filename='db.sqlite3')
#
# # @settings.HUEY.task()
# @task()
# def add(num, id):
# 	obj = DummyModel.objects.get(id=id)
#
# 	# return None
# 	total = 1
# 	for numm in range(100000000):
# 		total += numm * 10
# 	obj.integer += total
# 	obj.save()
