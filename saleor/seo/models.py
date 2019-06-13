from django.core.validators import MaxLengthValidator
from django.db import models


class SeoModel(models.Model):
    seo_title = models.CharField(
        max_length=100, blank=True, null=True,
        validators=[MaxLengthValidator(100)])
    seo_description = models.CharField(
        max_length=500, blank=True, null=True,
        validators=[MaxLengthValidator(500)])

    class Meta:
        abstract = True


class SeoModelTranslation(models.Model):
    seo_title = models.CharField(
        max_length=100, blank=True, null=True,
        validators=[MaxLengthValidator(100)])
    seo_description = models.CharField(
        max_length=500, blank=True, null=True,
        validators=[MaxLengthValidator(500)])

    class Meta:
        abstract = True
