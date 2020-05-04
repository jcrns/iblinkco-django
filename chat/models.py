from django.db import models
from django.contrib.auth.models import User
from service.models import JobPost
from django.db import connections

# Create your models here.l
class Message(models.Model):
    # job = models.ForeignKey(JobPost, on_delete=models.CASCADE )
    job = models.CharField(max_length=120, default='none')
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(job_id):

        # last_ten = Message.objects.filter(job=job_id).order_by('-timestamp')[:20]
        last_ten = self.objects.filter().order_by('-timestamp')
        last_ten = reversed(last_ten)
        print(last_ten)
        return last_ten

    connections.close_all()

    
# class Message(models.Model):
#     # job = models.ForeignKey(JobPost, on_delete=models.CASCADE )
#     job = models.CharField(max_length=120, default='none')
#     author = models.ForeignKey(
#         User, related_name='author_messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.author.username

#     def last_10_messages(job_id):

#         # last_ten = Message.objects.filter(job=job_id).order_by('-timestamp')[:20]
#         last_ten = Message.objects.filter(job=job_id).order_by('-timestamp')
#         last_ten = reversed(last_ten)
#         print(last_ten)
#         return last_ten

#     connections.close_all()

