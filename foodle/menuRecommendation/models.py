from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    spicy = models.FloatField()
    sweet = models.FloatField()
    bitter = models.FloatField()
    sour = models.FloatField()
    salty = models.FloatField()
    soup = models.BooleanField()

    class Meta:
        db_table=u'menu'