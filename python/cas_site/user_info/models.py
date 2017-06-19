from django.db import models

# Create your models here.
class Proj(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Repos(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Auth(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=20)
    repos = models.ForeignKey(Repos, on_delete=models.CASCADE, blank=True, null=True)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'repos', 'proj', 'level', 'group')

class Dir(models.Model):
    name = models.CharField(max_length=1000)
    repos = models.ForeignKey(Repos, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    auth = models.ForeignKey(Auth, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'repos', 'proj', 'level', 'group')
