from django.db import models
from django.contrib.auth.models import User


class userProfile(models.Model):
    mobie_number = models.CharField(max_length=70)
    dob = models.DateField()
    gender = models.CharField(max_length=70)
    is_admin = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    

class quiztopics(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_cat = models.CharField(max_length=255)
    quiz_title = models.CharField(max_length=255)
    quiz_desc = models.CharField(max_length=255)
    quiz_url = models.CharField(max_length=100,default="")
    quiz_thumb = models.ImageField(upload_to='MyQuiz/images')

class users(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=70)
    username = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=100)
    mobie_number = models.CharField(max_length=70)
    dob = models.DateField()
    gender = models.CharField(max_length=70)
    password = models.CharField(max_length=70)
    is_admin = models.BooleanField()


class quizquestion(models.Model):
    qn_id = models.AutoField(primary_key=True)
    qn_cat = models.CharField(max_length=255)
    qn_title = models.CharField(max_length=255)
    qn_name = models.CharField(max_length=255)
    qn_opt1 = models.CharField(max_length=255)
    qn_opt2 = models.CharField(max_length=255)
    qn_opt3 = models.CharField(max_length=255)
    qn_opt4 = models.CharField(max_length=255)
    qn_ans = models.CharField(max_length=255)

class useranswers(models.Model):
    qn_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=70)
    username = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=100)
    qn_cat = models.CharField(max_length=255)
    qn_name = models.CharField(max_length=255)
    qn_ans = models.CharField(max_length=255)
    crt_ans = models.CharField(max_length=255,default="")

