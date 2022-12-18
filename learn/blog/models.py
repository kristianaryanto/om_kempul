import email
from email.policy import default
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.text import slugify
# Create your models here.

class post(models.Model):
    title = models.CharField(max_length = 200,blank = True)
    body = models.TextField()
    categori = models.CharField(default='berita',max_length = 200)
    email = models.EmailField(default='name@gmail.com')
    regis_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank = True)
    def save(self):
        self.slug = slugify(self.title)
        super(post,self).save()
    
    def __str__(self):
        return "{}".format(self.title)


    class all_products(models.Model):
        def get_all_products():
            items = []
            with open('EXACT FILE PATH OF YOUR CSV FILE','r') as fp:
                # You can also put the relative path of csv file
                # with respect to the manage.py file
                reader1 = csv.reader(fp, delimiter=';')
                for value in reader1:
                    items.append(value)
            return items