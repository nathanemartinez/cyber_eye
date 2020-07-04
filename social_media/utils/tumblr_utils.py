from social_media.exceptions import InvalidCredentialsError


class GetTumblrData:
    def __init__(self, api, blog):
        try:
            self.api = api
        except:
            raise InvalidCredentialsError

        self.blog = blog

    def get_blog_info(self, high_quality_picture: bool = True):
        blog = self.api.blog_info(blogname=self.blog)
        base = blog['blog']
        info = {
            'blog_pic': base['avatar'][0]['url'],
            'description': base['description'],
            'is_nsfw': base['is_nsfw'],
            'username': base['name'],
            'num_posts': base['posts'],
            'header_image': base['theme']['header_image'],
            'title': base['title'],
            'url': base['url'],
        }
        return info

    def get_posts(self, high_quality_picture: bool = True):
        posts = self.api.posts(self.blog, limit=3)['posts']

        info = {}
        for i, post in enumerate(posts):
            base = posts[i]
            info[i] = {
                'type': base['type'],
                'date_created': base['date'],
                'tags': base['tags'],
                'post_url': base['short_url'],
            }
            if info[i]['type'] == 'photo':
                info[i]['image'] = base['photos'][0]['original_size']['url']
            elif info[i]['type'] == 'text':
                info[i]['summary'] = base['summary']
                info[i]['title'] = base['title']
                info[i]['text'] = base['trail'][0]['content_raw']
        return info

