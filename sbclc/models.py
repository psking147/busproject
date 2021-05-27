from django.db import models

# Create your models here.


class Stop(models.Model):
    index = models.PositiveIntegerField(default=111111)
    standard_id = models.PositiveIntegerField()
    ars = models.PositiveIntegerField()
    name = models.CharField(max_length=30)
    x = models.FloatField()
    y = models.FloatField()
    labels = models.PositiveIntegerField()
    congestion = models.PositiveIntegerField()
    before = models.PositiveIntegerField(null=True)
    after = models.PositiveIntegerField(null=True)
    xVector = models.FloatField(null=True)
    yVector = models.FloatField(null=True)

    def __str__(self):
        return self.name + '(' + str(self.ars) + ')'


class Line(models.Model):
    line_num = models.CharField(max_length=10)
    order = models.PositiveIntegerField()
    stop = models.PositiveIntegerField()
    stop_name = models.CharField(max_length=30, default='a')

    def __str__(self):
        return self.line_num + '(' + str(self.order) + ', ' + str(self.stop) + ')'


class LineCongestion(models.Model):
    line = models.CharField(max_length=10)
    congestion = models.PositiveIntegerField()

    def __str__(self):
        return self.line


class StopCongestion(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    c0 = models.PositiveIntegerField()
    c1 = models.PositiveIntegerField()
    c2 = models.PositiveIntegerField()
    c3 = models.PositiveIntegerField()
    c4 = models.PositiveIntegerField()
    c5 = models.PositiveIntegerField()
    c6 = models.PositiveIntegerField()
    c7 = models.PositiveIntegerField()
    c8 = models.PositiveIntegerField()
    c9 = models.PositiveIntegerField()
    c10 = models.PositiveIntegerField()
    c11 = models.PositiveIntegerField()
    c12 = models.PositiveIntegerField()
    c13 = models.PositiveIntegerField()
    c14 = models.PositiveIntegerField()
    c15 = models.PositiveIntegerField()
    c16 = models.PositiveIntegerField()
    c17 = models.PositiveIntegerField()
    c18 = models.PositiveIntegerField()
    c19 = models.PositiveIntegerField()
    c20 = models.PositiveIntegerField()
    c21 = models.PositiveIntegerField()
    c22 = models.PositiveIntegerField()
    c23 = models.PositiveIntegerField()

    def __str__(self):
        return self.stop.name + '(' + str(self.stop.ars) + ')'

