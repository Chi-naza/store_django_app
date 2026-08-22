from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


"""
This Tag Model and TagItem is an example of Generic Relationships. 
Instead of importing different models from other apps within our django project,
we instead create a generic foreign key, with fields we can use to trap and find any Object/Model we apply it to.
To Identify the parent object, we just need the type of the object, and the id of that object. With these we can lookup the DB

This means, it can be applied to any model object.


This same solution can be used to creat a Like Model with LikeItem, so with that, we can track what object a user likes

NB: this solution fails if the parent object uses a customId or field as a primary key i.e when primary key is not an integer.
"""

class Tag(models.Model):
    label = models.CharField(max_length=255)


class TagItem(models.Model):
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey() # this extra field is used to get the actual object this relationship is applied to