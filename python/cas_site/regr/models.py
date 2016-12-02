from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Proj(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='leader_fk', blank=True, null=True)
    dleader = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='dleader_fk', blank=True, null=True)
    vleader = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='vleader_fk', blank=True, null=True)
    def __str__(self):
        return self.name
    def pname(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    downer = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='downer_fk', blank=True, null=True)
    vowner = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='vowner_fk', blank=True, null=True)
    def __str__(self):
        return self.name
    def mname(self):
        return self.name.split('___')[0]
    def pname(self):
        return self.name.split('___')[1]

class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name
    def gname(self):
        return self.name.split('___')[0]
    def mname(self):
        return self.name.split('___')[1]
    def pname(self):
        return self.name.split('___')[2]

class Case(models.Model):
    name = models.CharField(max_length=500, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True)
    def __str__(self):
        return self.name
    def cname(self):
        return self.name.split('___')[0]
    def gname(self):
        return self.name.split('___')[1]
    def mname(self):
        return self.name.split('___')[2]
    def pname(self):
        return self.name.split('___')[3]

class Sim(models.Model):
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    proj_cl = models.CharField(max_length=20)
    seed = models.CharField(max_length=20)
    dut_ana_log = models.CharField(max_length=200)
    dut_ana_status = models.CharField(max_length=20)
    dut_ana_error = models.CharField(max_length=1000)
    tb_ana_log = models.CharField(max_length=200)
    tb_ana_status = models.CharField(max_length=20)
    tb_ana_error = models.CharField(max_length=1000)
    elab_log = models.CharField(max_length=200)
    elab_status = models.CharField(max_length=20)
    elab_error = models.CharField(max_length=1000)
    simu_log = models.CharField(max_length=200)
    simu_status = models.CharField(max_length=20)
    simu_error = models.CharField(max_length=1000)
    comp_cpu_time = models.CharField(max_length=20)
    simu_cpu_time = models.CharField(max_length=20)
    simu_time = models.CharField(max_length=20)
    def __str__(self):
        return str(self.pub_date)+'__'+self.simu_log
