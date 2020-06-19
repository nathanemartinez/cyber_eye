from social_media.exceptions import ProtectedUserError, InvalidScreenNameError
import tweepy


class GetTwitterData:
    def __init__(self, api, username):
        self.api = api
        self.username = username

        try:
            self.user_obj = api.get_user(screen_name=username)
            if self.user_obj.protected:
                raise ProtectedUserError(f'"{self.username}" is a protected user (private account).')
        except tweepy.TweepError:
            raise InvalidScreenNameError(f'"{self.username}" does not exist.')

        self.following = tweepy.Cursor(self.api.friends, screen_name=username, count=200).pages()
        self.followers = tweepy.Cursor(self.api.followers, screen_name=username, count=200).pages()

    def get_user_information(self):
        """
        reference: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        :param username: @TwitterUser - without the "@"
        :return: a list of user information
        """
        user = self.user_obj
        private_account = user.protected
        name = user.name
        follower_count = user.followers_count
        following_count = user.friends_count
        location = user.location
        url = user.url
        description = user.description
        liked_tweets = user.favourites_count
        tweets_retweets_count = user.statuses_count
        created_date_time = user.created_at
        info = [private_account, name, follower_count, following_count, location,
                url, description, liked_tweets, tweets_retweets_count,
                created_date_time]
        return info

    def get_user_profile_banner_urls(self):
        """
        Gets the user's profile image and banner image.
        :return: 2 bool vars that indicate if the image/banner urls are the default.
                 As well as 2 string vars containing the profile/banner url.
        """
        user = self.user_obj
        # Attribute 'profile_banner_url' breaks when user has a default theme
        # Get the theme image URL
        default_banner_url_bool = bool
        profile_banner_url = ''
        try:
            profile_banner_url = user.profile_banner_url
        except AttributeError:
            default_banner_url_bool = True
        else:
            default_banner_url_bool = False

        # Get the profile image URL
        default_profile_url_bool = bool
        default_profile_url = 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
        profile_image_url = ''
        try:
            profile_image_url = user.profile_image_url_https
            if profile_image_url == default_profile_url:
                default_profile_url_bool = True
            else:
                default_profile_url_bool = False
            pass
        except AttributeError:
            default_profile_url_bool = True

        info = [default_banner_url_bool, profile_banner_url,
                default_profile_url_bool, profile_image_url]
        return info

    def get_posts(self, count: int = 100, tweet_mode: str = 'extended',
                  exclude_replies: bool = False, include_retweets: bool = True):
        """
        Media reference: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/extended-entities-object
        Gets the user's tweets and retweets. As well as hashtags.
        I strongly recommend not including replies. Mentions will include them.
        :return:
        """
        posts = self.api.user_timeline(screen_name=self.username, count=count, exclude_replies=exclude_replies,
                                       include_rts=include_retweets, tweet_mode=tweet_mode)

        def _get_entity(the_tweet, get1: str, get2: str):
            """
            Used to get the hashtag or mentions within a tweet.
            :param the_tweet: the tweet.
            :return: hashtag or mentions list
            """
            the_list = the_tweet.entities.get(get1)
            return [dictionary.get(get2) for dictionary in the_list]

        def _get_highest_quality_video_link(url_list: list):
            """
            Gets the highest quality video link in the list.
            Goes for the highest pixel video.
            Uses the "100x100" pixels within the url.
            :param url_list: the list of urls
            :return: the highest quality video link.
            """
            url_list = set([string for string in url_list if '.m3u8' not in string])
            # string_list = list(set([string for string in string_list if '.m3u8' not in string]))
            dictionary = {}
            for string in url_list:
                size_list = string.split('/')[7].split('x')
                dictionary[string] = size_list[0], size_list[1]
            return max(dictionary, key=dictionary.get)

        def _get_media(tweet):
            """
            Gets media - videos, photos, gifs
            :param tweet: the tweet
            :return None if no media, (video type, url) if media
            """
            try:
                for media in tweet.extended_entities.get("media", [{}]):
                    if media.get("type", None) == "video":
                        # [1] because it's the clearest video
                        urls = [media["video_info"]["variants"][i]["url"] for i in range(4)]
                        video = _get_highest_quality_video_link(urls)
                        return 'video', video
                    elif media.get("type", None) == "photo":
                        photo = media['media_url_https']
                        return 'photo', photo
                    elif media.get("type", None) == "animated_gif":
                        gif = media["video_info"]["variants"][0]["url"]
                        return 'gif', gif
                    else:
                        return None
            except:
                return None

        def _run_posts(posts):
            """
            The "main" part of this class method.
            :param posts: user_timeline object
            :return: a list of tuples that contain the tweet text, hashtags, mentions, media
            """
            tweets = []
            for tweet in posts:
                text = "No tweet"
                # Gets text for a retweet
                try:
                    text = tweet.retweeted_status.full_text
                # Gets text for a tweet
                except AttributeError:
                    text = tweet.full_text
                finally:
                    hashtags = _get_entity(tweet, 'hashtags', 'text')
                    mentions = _get_entity(tweet, 'user_mentions', 'screen_name')
                    media = _get_media(tweet)
                    tweets.append((text, hashtags, mentions, media))

            return tweets

        info = _run_posts(posts)
        return info

    def get_media(self):
        """
        Gets the user's picture and video posts
        :return:
        """
        pass

    def get_likes(self):
        """
        Gets the user's liked posts.
        :return:
        """
        pass


class CleanText:
    pass


