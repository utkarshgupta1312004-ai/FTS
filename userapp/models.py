from django.utils import timezone
from adminapp.models import Employee
from django.db.models import BLANK_CHOICE_DASH
from django.db import models

# Create your models here.
class Files(models.Model):
    STATUS_CHOICE=[
        ("OPEN","Open"),
        ("IN_PROGRESS","In Progress"),
        ("CLOSED","Closed")
    ]
    file_no=models.CharField(max_length=30,unique=True,editable=False)
    title=models.CharField(max_length=50)
    subject=models.TextField(blank=True)
    initiated_by=models.ForeignKey(Employee,on_delete=models.PROTECT,related_name="intiated_files")
    current_holder=models.ForeignKey(Employee,on_delete=models.PROTECT,related_name="assigned_holder")
    file_attachment=models.FileField(upload_to="file",null="True",blank="True")
    status=models.CharField(max_length=20,choices=STATUS_CHOICE,default="OPEN")

    created_at=models.DateTimeField(auto_now_add=True)
    closed_at=models.DateTimeField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.file_no:
            year=timezone.now().year

            last_file=Files.objects.filter(
                file_no__startswith=f"file-{year}").order_by("-id").first()
            
            if last_file:
                try:
                    last_num=int(last_file.file_no.split("-")[-1])
                    new_num=last_num + 1
                except (IndexError,ValueError):
                    new_num=1
            else:
                new_num=1
            self.file_no=f"file-{year}-{new_num:04d}"
        super().save(*args, **kwargs)
    def __str__(self):
            return self.file_no
    
class FileMovement(models.Model):
    ACTION_CHOICES=[
        ("CREATE","Create"),
        ("FORWARD","Forward"),
        ("RETURN","Return"),
        ("CLOSE","Close"),
    ]
    file=models.ForeignKey(Files,on_delete=models.CASCADE,related_name="movements")
    from_employee=models.ForeignKey(Employee,on_delete=models.PROTECT,null=True,related_name="sent_files",blank=True)
    to_employee=models.ForeignKey(Employee,on_delete=models.PROTECT,null=True,related_name="received_files",blank=True)
    action=models.CharField(max_length=20,choices=ACTION_CHOICES)
    remark=models.TextField(blank=True)
    moved_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["moved_at"]
            
            
