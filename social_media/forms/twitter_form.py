from django import forms
from social_media.models.twitter_model import TwitterSpider


class TwitterSpyderForm(forms.ModelForm):
    class Meta:
        model = TwitterSpider
        fields = ['twitter_user']
