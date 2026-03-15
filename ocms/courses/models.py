from django.db import models
from accounts.models import User
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    level = models.CharField(max_length=50)
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    def __str__(self):
        return self.title
class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.URLField(max_length=500, null=True, blank=True)
    resources_url = models.URLField(max_length=500, null=True, blank=True)
    lecture_type = models.CharField(max_length=20, default='video') # video, lab, quiz
    notes = models.TextField()
    order = models.IntegerField()
    duration = models.IntegerField()
    def __str__(self):
        return self.title