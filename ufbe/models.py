from django.db import models

# Create your models here.

class Pictures(models.Model):
  pictureId = models.AutoField(primary_key=True, serialize=True)
  pictureData = models.TextField(default="https://static.wixstatic.com/media/b77fe464cfc445da9003a5383a3e1acf.jpg")
  word = models.CharField(max_length=255, default="blank")

class Users(models.Model):
  username = models.CharField(max_length=50, primary_key=True)
  avatarUrl = models.CharField(max_length=255, default="https://www.kindpng.com/picc/m/421-4212275_transparent-default-avatar-png-avatar-img-png-download.png")
  language = models.CharField(max_length=50, default="english")
  score = models.IntegerField(default=0)
  img = models.ForeignKey(Pictures, on_delete=models.CASCADE)
