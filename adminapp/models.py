from django.db import models
import datetime

# Create your models here.
class Department(models.Model):
    deptid=models.AutoField(primary_key=True)
    deptname=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.deptname

class Employee(models.Model):
    empid=models.CharField(max_length=20)
    empname=models.CharField(max_length=100)
    empemail=models.CharField(max_length=100,primary_key=True)
    empdiscription=models.CharField(max_length=100)
    empdept=models.ForeignKey(Department,on_delete=models.CASCADE)
    joindate=models.DateField(default=datetime.date.today)
    pictures=models.ImageField(upload_to='profileimg/',default='images/default.jpg')

    def __str__(self):
        return self.empname



