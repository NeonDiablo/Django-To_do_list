from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Task(models.Model):

    colors_list = [
        ('border-primary','Blue'),
        ('border-secondary','Gray'),
        ('border-success','Green'),
        ('border-danger','Red'),
        ('border-warning','Yellow'),
        ('border-info','Light Blue'),
        ('border-dark','Black'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    colors = models.CharField(max_length=20, choices=colors_list, default='blue_bootstrp')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task/', {'pk':self.pk})

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['updated_at']

    
