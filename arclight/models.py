from djongo import models

class NLUModel(models.Model):

    _id = models.ObjectIdField()
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    model_directory = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.name

class Intent(models.Model):

    _id = models.ObjectIdField()
    nlu_model = models.ForeignKey(
        NLUModel,
        on_delete=models.CASCADE,
        related_name = 'intents',
    )
    name = models.CharField(max_length=128, blank=False)
    phrases = models.ListField(models.CharField(max_length=256))
    answers = models.ListField(models.CharField(max_length=256))

    def __str__(self):
        return self.name
