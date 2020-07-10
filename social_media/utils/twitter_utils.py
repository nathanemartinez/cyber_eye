from social_media.exceptions import (ProtectedUserError,
                                     InvalidScreenNameError, InvalidCredentialsError)
import tweepy


class GetTwitterData:
    def __init__(self, api, username):
        try:
            self.api = api
        except tweepy.TweepError:
            raise InvalidCredentialsError

        self.username = username

    def get_user_obj(self):
        try:
            user_obj = self.api.get_user(screen_name=self.username)
            if user_obj.protected:
                raise ProtectedUserError
        except tweepy.TweepError:
            raise InvalidScreenNameError
        return user_obj

    def get_user_information(self):
        """
        Gets basic user information
        Reference: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        :return: a dictionary of user information
        """
        user = self.get_user_obj()

        name, location, description = self._remove_emojis([user.name, user.location, user.description])

        info = {
            "private": user.protected,
            "follower_count": user.followers_count,
            "following_count": user.friends_count,
            "liked_tweets": user.favourites_count,
            "tweets_retweets_count": user.statuses_count,

            "created_datetime": user.created_at,
            "url": user.url or None,
            "name": name or None,
            "location": location or None,
            "description": description or None,
        }

        info = {str(key): str(value) for key, value in info.items()}
        return info

    def get_following(self, count: int = 5):
        """
        Get a user object for each person the user is following.
        User obj reference: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        :param count: how many followers to retrieve
        :return: cursor object that contains a list of user objects
        """
        return tweepy.Cursor(self.api.friends, screen_name=self.username).items(count)

    def get_followers(self, count: int = 5):
        """ Same as ".get_following" but with the user's followers """
        return tweepy.Cursor(self.api.followers, screen_name=self.username).items(count)

    def get_user_profile_banner_urls(self, high_quality_profile_picture: bool = True):
        """
        Gets the user's profile image and banner image.
        :param high_quality_profile_picture: True will get the originally uploaded profile picture
            which might be big in file size
        :return: A dictionary containing 2 bool vars that indicate if the image/banner urls are the default.
            As well as 2 string vars containing the profile/banner url.
        """
        user = self.get_user_obj()

        def _get_banner_image():
            try:
                return user.profile_banner_url  # some user objs do not have that attribute
            except AttributeError:
                return None

        def _get_profile_image():
            try:
                default_url = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
                profile_url = user.profile_image_url_https
                if profile_url == default_url:
                    return None
                else:
                    if high_quality_profile_picture:
                        profile_url = profile_url.replace('_normal', '')
                    return profile_url
                pass
            except AttributeError:
                return None

        info = {
            'banner_pic': _get_banner_image(),
            'profile_pic': _get_profile_image(),
        }
        return info

    def get_posts(self, count: int = 5, tweet_mode: str = 'extended',
                  exclude_replies: bool = True, include_retweets: bool = False,
                  high_quality_videos: bool = True):
        """
        Media reference: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/extended-entities-object
        Gets the user's tweets and retweets. As well as hashtags.
        I strongly recommend not including replies. Mentions will include them.

        :param count: how many tweets to get
        :param tweet_mode: if not 'extended' then the tweets will be truncated
        :param exclude_replies: false = include replies
        :param include_retweets: true = include retweets
        :param high_quality_videos: true = get the highest quality video
        :return:
        """
        posts = self.api.user_timeline(screen_name=self.username, count=count, exclude_replies=exclude_replies,
                                       include_rts=include_retweets, tweet_mode=tweet_mode)

        def _get_entity(tweet, get1: str, get2: str):
            """
            Used to get the hashtag or mentions within a tweet.
            :param tweet: the tweet.
            :return: hashtag or mentions list
            """
            entity_list = tweet.entities.get(get1)
            return [dictionary.get(get2) for dictionary in entity_list]

        def _get_video_link(urls: list, high_quality: bool = True):
            """
            Gets the highest or lowest quality video link
            Uses the "100x100" pixels within the url.
            :param urls: the list of urls
            :return: the highest quality video link.
            """
            urls = set([string for string in urls if '.m3u8' not in string])
            dictionary = {}
            for string in urls:
                size_list = string.split('/')[7].split('x')
                if high_quality:
                    size = max(list(map(int, size_list)))
                else:
                    size = min(list(map(int, size_list)))
                dictionary[string] = size
            if high_quality:
                return max(dictionary, key=dictionary.get)
            else:
                return min(dictionary, key=dictionary.get)

        def _get_media(tweet):
            """
            Gets media - videos, photos, gifs
            :param tweet: the tweet
            :return None if no media, (video type, url) if media
            """
            try:
                for media in tweet.extended_entities.get("media", [{}]):
                    if media.get("type", None) == "video":
                        urls = [media["video_info"]["variants"][i]["url"] for i in range(4)]
                        return 'video', _get_video_link(urls, high_quality_videos)
                    elif media.get("type", None) == "photo":
                        return 'photo', media['media_url_https']
                    elif media.get("type", None) == "animated_gif":
                        return 'gif', media["video_info"]["variants"][0]["url"]
                    else:
                        return None
            except:
                return None

        def _run(posts):
            """
            The "main" part of this class method.
            :param posts: user_timeline object
            :return: a list of tuples that contain the tweet text, hashtags, mentions, media
            """
            tweets = {}
            for i, tweet in enumerate(posts):
                text = None
                try:
                    text = tweet.retweeted_status.full_text
                except AttributeError:
                    text = tweet.full_text
                finally:
                    hashtags = _get_entity(tweet, 'hashtags', 'text')
                    mentions = _get_entity(tweet, 'user_mentions', 'screen_name')
                    media = _get_media(tweet)
                    tweet_url = f'https://twitter.com/user/status/{tweet.id}'
                    tweets[i] = (tweet_url, text, hashtags, mentions, media)
            return tweets

        info = _run(posts)
        return info

    @staticmethod
    def _remove_emojis(string_list):
        """
        :param string_list: list of strings
        :return: a list of strings with no emojis
        """
        for index, string in enumerate(string_list):
            if string:
                string_list[index] = string.encode('ascii', 'ignore').decode('ascii').replace('\n', '')
        return string_list
