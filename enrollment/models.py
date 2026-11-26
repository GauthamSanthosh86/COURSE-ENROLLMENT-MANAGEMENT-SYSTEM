from django.db import models

# Create your models here.
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    duration_months = models.IntegerField()
    enrollment_date = models.DateField()
    fee = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Active'
    )