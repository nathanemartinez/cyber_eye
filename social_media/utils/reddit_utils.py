from social_media.exceptions import (InvalidCredentialsError, InvalidUserError,
                                     SuspendedBannedAccountError)
from prawcore.exceptions import (OAuthException, RequestException,
                                 ResponseException, NotFound)


class GetRedditData:
    def __init__(self, api, username: str):
        try:
            self.api = api
        except (OAuthException, RequestException, ResponseException):
            raise InvalidCredentialsError
        self.username = username
        try:
            user_obj = self.api.redditor(self.username)
            if hasattr(user_obj, 'is_suspended'):
                raise SuspendedBannedAccountError
            self.user = user_obj
        except NotFound:
            raise InvalidUserError

    def get_user_information(self):
        """
        Gets basic user info such as their profile picture and information
        about their subreddit (if they have one).
        :return: a dictionary
        """
        info = {
            'comment_karma': self.user.comment_karma,
            'link_karma': self.user.link_karma,
            'total_karma': self.user.comment_karma + self.user.link_karma,
            'created': self.user.created_utc,
            'profile_pic': self.user.icon_img,
        }
        if hasattr(self.user, 'subreddit'):
            info['sub_banner_img'] = self.user.subreddit['banner_img']
            info['sub_over_18'] = self.user.subreddit['over_18']
            info['sub_description'] = self.user.subreddit['public_description']
            info['sub_subs'] = self.user.subreddit['subscribers']
            info['sub_title'] = self.user.subreddit['title']
        return info

    def get_comments(self, limit: int = 20, sort_by: str = 'new'):
        """
        Reference: https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
        :param limit: how many comments to get (inclusive) - 'None' will get 1000 posts
        :param sort_by: sort by controversial, hot, top, or new comments
        :return: a comment object
        """
        def _get_info(comments):
            info = {}
            for i, comment in enumerate(comments):
                info[i] = {
                    'text': comment.body,
                    'created_utc': comment.created_utc,
                    'is_post_author': comment.is_submitter,
                    'link': f'https://www.reddit.com{comment.permalink}'.replace(comment.id, '').rstrip('/'),
                    'comment_forest_obj': comment.replies,
                    'upvotes': comment.score,
                    'submission_obj': comment.submission,
                    'subreddit_obj': comment.subreddit,
                    'subreddit_link': f'https://www.reddit.com/r/{comment.subreddit}/'
                }
            return info

        if sort_by == 'controversial':
            comments = self.user.comments.controversial(limit=limit)
            return _get_info(comments)
        elif sort_by == 'hot':
            comments = self.user.comments.hot(limit=limit)
            return _get_info(comments)
        elif sort_by == 'top':
            comments = self.user.comments.top(limit=limit)
            return _get_info(comments)
        else:
            comments = self.user.comments.new(limit=limit)
            return _get_info(comments)

    def get_posts(self, limit: int = 20, sort_by: str = 'new'):
        """
        Reference: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
        :param limit: how many submissions to get (inclusive) - 'None' will get 1000 posts
        :param sort_by: sort by controversial, hot, top, or new submissions
        :return: a submission object
        """
        def _get_info(posts):
            info = {}
            for i, post in enumerate(posts):
                info[i] = {
                    'author': post.author,
                    'comment_obj': post.comments,
                    'created_utc': post.created_utc,
                    'text_only': post.is_self,
                    'num_comments': post.num_comments,
                    'over_18': post.over_18,
                    'upvotes': post.score,
                    'text': post.selftext or None,
                    'title': post.title or None,
                    'upvote_ratio': post.upvote_ratio,
                    'url': post.url,
                    'subreddit_obj': post.subreddit,
                    'subreddit_link': f'https://www.reddit.com/r/{post.subreddit}/'
                }
            return info

        if sort_by == 'controversial':
            posts = self.user.submissions.controversial(limit=limit)
            return _get_info(posts)
        elif sort_by == 'hot':
            posts = self.user.submissions.hot(limit=limit)
            return _get_info(posts)
        elif sort_by == 'top':
            posts = self.user.submissions.top(limit=limit)
            return _get_info(posts)
        else:
            posts = self.user.submissions.new(limit=limit)
            return _get_info(posts)

