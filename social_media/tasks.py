# from huey import SqliteHuey
from huey.contrib.djhuey import task
# huey = SqliteHuey(filename='db.sqlite3')
# @settings.HUEY.task()


"""
For some reason, you're only allowed to import stuff within the function.
"""


@task()
def add(num, id):
	from social_media.models.twitter_model import DummyModel
	obj = DummyModel.objects.get(id=id)
	obj.integer += num
	obj.save()
	return num


@task()
def get_info(twitter_user, pk):
	from social_media.models.twitter_model import TwitterSpider, TwitterApiKey
	from social_media.utils.twitter_utils import GetTwitterData
	import json

	obj = TwitterSpider.objects.get(pk=pk)
	api = TwitterApiKey.objects.first().get_api()
	spider = GetTwitterData(api, str(twitter_user))

	info = spider.get_user_information()
	obj.user_info = json.dumps(info)
	info = spider.get_user_profile_banner_urls()
	obj.user_profile_pictures = json.dumps(info)
	obj.save()
	return None


@task()
def get_followers_or_following(twitter_user, num_people, user, pk):
	from social_media.models.twitter_model import TwitterSpider, TwitterApiKey
	from social_media.utils.twitter_utils import GetTwitterData

	obj = TwitterSpider.objects.get(pk=pk)
	api = TwitterApiKey.objects.first().get_api()
	spider = GetTwitterData(api, str(twitter_user))

	def _upload_file(path, info):
		with open(path, 'w', newline='') as file:
			users = [person.screen_name for person in info]
			for person in users:
				file.write(f'{person}\n')

	info = spider.get_followers(count=num_people)
	path = f'social_media/media/social_media/twitter/followers/{user}_{twitter_user}.txt'
	_upload_file(path, info)
	obj.followers = path

	info = spider.get_following(count=num_people)
	path = f'social_media/media/social_media/twitter/following/{user}_{twitter_user}.txt'
	_upload_file(path, info)
	obj.following = path

	obj.save()
	return None
