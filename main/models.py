from django.db import models


class Exercise(models.Model):
    title = models.CharField("Номер в общем списке", max_length=50)
    short_description = models.CharField("Краткое описание", max_length=250)
    text = models.TextField("Решение или мб описание")
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title



