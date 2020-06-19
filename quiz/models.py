from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     is_taker = models.BooleanField(default=True)
#     is_creator = models.BooleanField(default=False)
#

# class QuizType(models.Model):
#     name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.answer


# class Taker(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     quizzes = models.ManyToManyField(Quiz)
#
#     def __str__(self):
#         return self.user.username

#
# class TakenQuiz(models.Model):
#     taker = models.ForeignKey(Taker, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.taker


# class TakerAnswer(models.Model):
#     taker = models.ForeignKey(Taker, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)



# class Test(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default='Nonee')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=100, default='test')
    # description = models.TextField(max_length=200, default='')
    # created = models.DateTimeField(auto_now=True)
    #
    # def __str__(self):
    #     return self.title

#
# class Question(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     description = models.TextField(max_length=1000, blank=True)
#     contains_numbers = models.BooleanField(default=False)
#     question = models.CharField(max_length=500)
#
#     def __str__(self):
#         return self.question
#
#
# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer_text = models.CharField(max_length=200, default='')
#     answer_number = models.IntegerField(default=999999)
#     # if question.contains_numbers:
#     #     choice = models.IntegerField()
#     # else:
#     #     choice = models.CharField(max_length=200)
#
#     def __str__(self):
#         return f"{self.question} - Answer"
#     #
#     # def save():
#     #     question.id
#     #     if question.contains....
#     #
#
#
# class QuizTaker(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username
#
#
