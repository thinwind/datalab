from django.db import models
from . import components

class Param:
    def __init__(self,key,source=None,title='参数',generator=generators.identity_text_generator):
        self.key = key
        self.source = source
        self.title = title
        self.generator = generator
        self.value =generator(source)


class Machine(models.Model):
    name = models.CharField(max_length=200,blank=False,default="新生产机")
    input_params = models.TextField(blank=True)
    engine = models.CharField(max_length=100,blank=False)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True,default="新生产机")
    owner = models.ForeignKey('auth.User',related_name='machies',on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=True)

class AssemblyLine(models.Model):
    name = models.CharField(max_length=200,blank=False,default='新生产线')
    imput_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True,default="新生产线")
    sub_assemblylines = models.ManyToManyField('self',symmetrical=False,through='SubAssemblyLine',
            through_fields=('assemblyline','sub_line'))
    machines = models.ManyToManyField(Machine,through='MachineGroup',through_fields=('assemblyline','machine'))

class SubAssemblyLine(models.Model):
    assemblyline = models.ForeignKey(AssemblyLine,on_delete=models.CASCADE)
    sub_line = models.ForeignKey(AssemblyLine,on_delete=models.CASCADE)
    postion = models.IntegerField()

class MachineGroup(models.Model):
    assemblyline = models.ForeignKey(AssemblyLine,on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
    postion = models.IntegerField()