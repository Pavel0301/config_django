# Create your models here.
"""
class Room(models.Model):
    name = models.CharField(max_length=20, blank=False)
    slug = models.SlugField(max_length=10)


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add)
"""