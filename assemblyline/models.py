from django.db import models
from . import components

class Param:
    def __init__(self,key,source=None,title='参数',generator=components.identity_text_generator):
        self.key = key
        self.source = source
        self.title = title
        self.generator = generator
        self.value =generator(source)


class Machine(models.Model):
    class Meta:
        db_table='al_machine'
    name = models.CharField(max_length=200,blank=False,default="新生产机")
    input_params = models.TextField(blank=True)
    engine = models.CharField(max_length=100,blank=False)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True,default="新生产机")
    status = models.IntegerField(default=1)
    owner = models.ForeignKey('auth.User',related_name='machies',on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class CompoundMachine(models.Model):
    class Meta:
        db_table='al_compound_machine'
    name = models.CharField(max_length=200,blank=False,default="新复合生产机")
    input_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True,default="新复合生产机")
    sub_machines = models.ManyToManyField(Machine,related_name='compound_machies',through='MachineGroup')
    status = models.IntegerField(default=1)
    owner = models.ForeignKey('auth.User',related_name='compound_machies',on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class MachineGroup(models.Model):
    class Meta:
        db_table='al_machine_group'
    compound_machine = models.ForeignKey(CompoundMachine,on_delete=models.CASCADE)
    sub_machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
    postion = models.IntegerField()

class AssemblyLine(models.Model):
    class Meta:
        db_table='al_assembly_line'
    name = models.CharField(max_length=200,blank=False,default='新生产线')
    imput_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True,default="新生产线")
    machines = models.ManyToManyField(Machine,through='AssemblyLineMachine',
            through_fields=('assembly_line','machine'),related_name='assembly_lines')
    compound_machines = models.ManyToManyField(CompoundMachine,through='AssemblyLineCompoundMachine',
            through_fields=('assembly_line','compound_machine'),related_name='assembly_lines')
    status = models.IntegerField(default=1)
    owner = models.ForeignKey('auth.User',related_name='assembly_lines',on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class AssemblyLineMachine(models.Model):
    class Meta:
        db_table='al_assembly_line_machine'
    assembly_line = models.ForeignKey(AssemblyLine,on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
    postion = models.PositiveSmallIntegerField()

class AssemblyLineCompoundMachine(models.Model):
    class Meta:
        db_table='al_assembly_line_compound_machine'
    assembly_line = models.ForeignKey(AssemblyLine,on_delete=models.CASCADE)
    compound_machine = models.ForeignKey(CompoundMachine,on_delete=models.CASCADE)
    postion = models.PositiveSmallIntegerField()