from django.db import models

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} {str(self.address)} {str(self.work)} {str(self.age)}'