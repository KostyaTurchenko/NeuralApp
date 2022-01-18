from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    
    def __str__(self):
        return self.title


class Config(models.Model):
    diagram = models.CharField(max_length=100, default='bar')
    dropout = models.CharField(max_length=100, default='0.5')
    accuracy = models.CharField(max_length=100, default='off')
    # image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.diagram