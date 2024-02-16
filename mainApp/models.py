from django.db import models


class Receptionist(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=150, default='')
    city = models.CharField(max_length=150, default='')
    state = models.CharField(max_length=150, default='')
    password = models.CharField(max_length=50, default='12345')
    date_of_creation = models.DateField(null=True, blank=True)
    createdBy = models.CharField(max_length=50, null=True, blank=True)
    last_updated = models.CharField(max_length=50, blank=True, null=True)
    who_updated = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.name)+" / "+self.email
    
# choice = ((1, "Business Visit"), (2, "Personal Visit"), (3, "Job Visit"), (4, "Others"))

class VisitReason(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"



class Visitor(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    # purpose = models.IntegerField(choices=choice)
    purpose = models.ForeignKey(VisitReason, on_delete=models.CASCADE)
    to_meet = models.CharField(max_length=50)
    date_of_visit = models.DateField()
    createdBy = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, default='')
    last_updated = models.CharField(max_length=50, blank=True, null=True)
    who_updated = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name + " / " + self.email + " / " + self.to_meet