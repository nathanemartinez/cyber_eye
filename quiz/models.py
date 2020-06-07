from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='test')
    description = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=True)
    contains_numbers = models.BooleanField(default=False)
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # if question.contains_numbers:
    #     choice = models.IntegerField()
    # else:
    #     choice = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.question} - Answer"


class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


