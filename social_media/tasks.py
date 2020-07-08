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
def get_user_information(spider, user, twitter_user):
	from social_media.models.twitter_model import TwitterSpider
	import json
	obj = TwitterSpider.objects.get(user=user, twitter_user=twitter_user)
	obj.user_info = json.dumps(spider.get_user_information())
	obj.save()
	return None


@task()
def get_user_profile_banner_urls(spider, user, twitter_user):
	from social_media.models.twitter_model import TwitterSpider
	import json
	obj = TwitterSpider.objects.get(user=user, twitter_user=twitter_user)
	obj.user_profile_pictures = json.dumps(spider.get_user_profile_banner_urls())
	obj.save()
	return None


@task()
def get_followers_or_following(spider, user, twitter_user, num_people):
	from social_media.models.twitter_model import TwitterSpider
	obj = TwitterSpider.objects.get(user=user, twitter_user=twitter_user)

	def _upload_file(path, info_dict):
		with open(path, 'w', newline='') as file:
			users = [user_obj_list.screen_name for user_obj_list in info_dict]
			for person in users:
				file.write(f'{person}\n')

	info_dict = spider.get_followers(count=num_people)
	path1 = f'social_media/media/social_media/twitter/followers/{user}_{spider.username}.txt'
	_upload_file(path1, info_dict)

	info_dict = spider.get_following(count=num_people)
	path2 = f'social_media/media/social_media/twitter/following/{user}_{spider.username}.txt'
	_upload_file(path2, info_dict)
	info = {'followers': path1, 'following': path2}
	obj.followers = path1
	obj.following = path2
	obj.save()
	return info


