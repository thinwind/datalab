from django.db import models
from . import components


class Machine(models.Model):
    class Meta:
        db_table = 'al_machine'
    name = models.CharField(max_length=200, blank=False, default="新生产机")
    input_params = models.TextField(blank=True)
    engine_type = models.CharField(max_length=100, blank=False)
    engine_body = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    product_model = models.CharField(max_length=20,blank=False,default='merge')
    description = models.TextField(blank=True, default="新生产机")
    status = models.IntegerField(default=1)
    owner = models.ForeignKey(
        'auth.User', related_name='machies', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class CompoundMachine(models.Model):
    class Meta:
        db_table = 'al_compound_machine'
    name = models.CharField(max_length=200, blank=False, default="新复合生产机")
    input_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True, default="新复合生产机")
    sub_machines = models.ManyToManyField(
        Machine, related_name='compound_machies', through='MachineGroup')
    status = models.IntegerField(default=1)
    owner = models.ForeignKey(
        'auth.User', related_name='compound_machies', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class MachineGroup(models.Model):
    class Meta:
        db_table = 'al_machine_group'
    compound_machine = models.ForeignKey(
        CompoundMachine, on_delete=models.CASCADE)
    sub_machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    postion = models.IntegerField()


class AssemblyLine(models.Model):
    class Meta:
        db_table = 'al_assembly_line'
    name = models.CharField(max_length=200, blank=False, default='新生产线')
    imput_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    description = models.TextField(blank=True, default="新生产线")
    machines = models.ManyToManyField(Machine, through='AssemblyLineMachine',
                                      through_fields=('assembly_line', 'machine'), related_name='assembly_lines')
    compound_machines = models.ManyToManyField(CompoundMachine, through='AssemblyLineCompoundMachine',
                                               through_fields=('assembly_line', 'compound_machine'), related_name='assembly_lines')
    status = models.IntegerField(default=1)
    owner = models.ForeignKey(
        'auth.User', related_name='assembly_lines', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class AssemblyLineMachine(models.Model):
    class Meta:
        db_table = 'al_assembly_line_machine'
    assembly_line = models.ForeignKey(AssemblyLine, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    postion = models.PositiveSmallIntegerField()


class AssemblyLineCompoundMachine(models.Model):
    class Meta:
        db_table = 'al_assembly_line_compound_machine'
    assembly_line = models.ForeignKey(AssemblyLine, on_delete=models.CASCADE)
    compound_machine = models.ForeignKey(
        CompoundMachine, on_delete=models.CASCADE)
    postion = models.PositiveSmallIntegerField()


class ProductLine(models.Model):
    """
        产品线模型
        一旦生产线组装完成，就生成一条产品线，产品线就是一组直接进行数据生产的
        Machine组成，在使用生产线进行生产时，直接使用产品线进行生产
    """
    class Meta:
        db_table = 'al_product_line'
    assembly_line = models.OneToOneField(
        AssemblyLine, on_delete=models.CASCADE)
    input_params = models.TextField(blank=True)
    output_params = models.TextField(blank=True)
    machies = models.ManyToManyField(Machine, related_name='+', through='ProductLineMachine', through_fields=(
        'product_line', 'machine'))


class ProductLineMachine(models.Model):
    class Meta:
        db_table = 'al_product_line_machine'
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    postion = models.PositiveSmallIntegerField()
