from email.policy import default
from django.db import models

# Create your models here.

class Csv(models.Model):
 
    file_name = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{}".format(self.file_name)



class human():
    def __init__(self, myname):
        self.filename = myname


class db_target_conf(models.Model):
    dbfrom = models.CharField(max_length = 300)
    table_name = models.CharField(max_length = 300)
    query  = models.CharField(max_length = 300)

# class inp(models.Model):
#     def __init__(self,input):
#         self.input = input
#         [name] = self.input

#         globals()[name] = models.CharField(max_length = 200)
#         print(self.input)


# ani = type('inp2',(models.Model,),{"__module__"})