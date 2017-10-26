"""pj app  models """
from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class User(models.Model):
    """ User models """
    name = models.CharField(max_length=20, unique=True)
    asic_info = JSONField(default=dict, blank=True)
    def __str__(self):
        return self.name

class Proj(models.Model):
    """ Project models """
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
        """ get project name"""
        return self.name

class Module(models.Model):
    """ Module models """
    name = models.CharField(max_length=100, unique=True)
    downer = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='downer_fk', blank=True, null=True)
    vowner = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='vowner_fk', blank=True, null=True)
    def __str__(self):
        return self.name
    def mname(self):
        """ get module name"""
        return self.name.split('___')[0]
    def pname(self):
        """ get project name"""
        return self.name.split('___')[1]

##### regression model #####
class RegrSimv(models.Model):
    """ regr simv models """
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name
    def vname(self):
        """ get verification person name"""
        return self.name.split('___')[0]
    def mname(self):
        """ get module name"""
        return self.name.split('___')[1]
    def pname(self):
        """ get project name"""
        return self.name.split('___')[2]

class RegrCase(models.Model):
    """ regr case models """
    name = models.CharField(max_length=500, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True)
    def __str__(self):
        return self.name
    def cname(self):
        """ get case name"""
        return self.name.split('___')[0]
    def vname(self):
        """ get verification person name"""
        return self.name.split('___')[1]
    def mname(self):
        """ get module name"""
        return self.name.split('___')[2]
    def pname(self):
        """ get project name"""
        return self.name.split('___')[3]

class RegrSim(models.Model):
    """ regr sim models """
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    m_name = models.CharField(max_length=20)
    simv = models.ForeignKey(RegrSimv, on_delete=models.CASCADE)
    v_name = models.CharField(max_length=20)
    case = models.ForeignKey(RegrCase, on_delete=models.CASCADE)
    c_name = models.CharField(max_length=100)
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
    regr_types = models.CharField(max_length=200)
    def __str__(self):
        return str(self.pub_date)+'__'+self.simu_log

##### dc model #####
class DcRun(models.Model):
    """ Dc models """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    m_name = models.CharField(max_length=20)
    clock = models.CharField(max_length=20)
    cpu_time = models.CharField(max_length=20)
    run_time = models.DateTimeField(unique=True)
    dc_log = models.CharField(max_length=200)
    error_info = JSONField(default=dict, blank=True)
    warning_info = JSONField(default=dict, blank=True)
    time_rpt = JSONField(default=dict, blank=True)
    qor_rpt = JSONField(default=dict, blank=True)
    power_rpt = JSONField(default=dict, blank=True)
    def __str__(self):
        return str(self.user)+str(self.run_time)

##### fm model #####
class FmRun(models.Model):
    """ Fm models """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    m_name = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    run_time = models.DateTimeField(unique=True)
    def __str__(self):
        return str(self.run_time)

##### MP model #####
class MpRun(models.Model):
    """ Mp models """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proj = models.ForeignKey(Proj, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    m_name = models.CharField(max_length=20)
    run_time = models.DateTimeField()
    pj_props = JSONField()
    props = JSONField()
    misc = JSONField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    def __str__(self):
        return str(self.pj_props)

class Comment(models.Model):
    """user Comments """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    pub_time = models.CharField(max_length=25, unique=True)
    