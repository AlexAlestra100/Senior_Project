from itertools import product
from django.db import models

class StatusHistory(models.Model):
   status_history_ID = models.AutoField(primary_key=True)
   activity_ID = models.ForeignKey('Activity', on_delete=models.CASCADE)
   status = models.CharField(max_length=50)
   date_time = models.DateTimeField(auto_now_add=True)

   class Meta:
      verbose_name = 'Status History'
      verbose_name_plural = 'Status History'

   def __str__(self):
      return str(self.status_history_ID)
   
#-----------------------------------------------------
#status table
class Status(models.Model):
   #status choices 
   option_choice = [
      ('Accept', "accept"),
      ('Reschedule', "reschedule"),
      ('Request', "request"),
      ('Cancel', "cancel"),
      ('Decline', 'decline'),
      ('Expire', 'expire'),
   ]
   #status table
   Status_ID = models.AutoField(primary_key=True)
   status= models.CharField(max_length=50, choices = option_choice, default = 'Request')
   class Meta: 
      verbose_name ='Statu'
   def __str__(self):       
      return str(self.status)
#----------------------------------------------

class UserRole(models.Model):
   roles_ID = models.AutoField(primary_key=True)
   name = models.CharField(max_length=50)

   class meta:
      verbose_name_plural = 'User Roles'

   def __str__(self):
      return self.name

class Product(models.Model):
   product_ID = models.AutoField(primary_key=True)
   external_product_ID = models.CharField(max_length=50, blank=True, null=True)
   name = models.CharField(max_length=100)

   class meta:
      verbose_name = 'Product'
      verbose_name_plural = 'Products'

   def __str__(self):
      return self.name

class Proficiency(models.Model):
   proficiency_ID = models.AutoField(primary_key=True)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   level = models.IntegerField(default=1)

   class meta:
      verbose_name = 'Proficiency'
      verbose_name_plural = 'Proficiencies'

   def __str__(self):
      return self.product.name + " " + str(self.level)

class PresalesMember(models.Model):
   presales_member_ID = models.AutoField(primary_key=True)
   external_presales_member_ID = models.CharField(max_length=50)
   user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, blank=True, null=True)
   proficiency = models.ManyToManyField(Proficiency)

   class meta:
      verbose_name = 'Presales Member'
      verbose_name_plural = 'Presales Members'

   def __str__(self):
      return str(self.presales_member_ID)

class Activity(models.Model):
   activity_ID = models.AutoField(primary_key=True)
   opportunity_ID = models.CharField(max_length=100)
   createdByMember = models.ForeignKey(PresalesMember, on_delete=models.CASCADE, blank=True, null=True, related_name='createdByMember')
   members = models.ManyToManyField(PresalesMember, blank=True)
   oneDateTime = models.DateTimeField(blank=True, null=True, help_text = "Year-Month-Day Hour:Minute:Second")
   twoDateTime = models.DateTimeField(blank=True, null=True, help_text = "Year-Month-Day Hour:Minute:Second")
   threeDateTime = models.DateTimeField(blank=True, null=True, help_text = "Year-Month-Day Hour:Minute:Second")
   selectedDateTime = models.DateTimeField(blank=True, null=True, help_text = "Year-Month-Day Hour:Minute:Second")
   products = models.ManyToManyField(Product)
   description = models.CharField(blank=True, null=True, max_length=500)
   status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
   flag = models.BooleanField(default=False)

   class meta:
      verbose_name_plural = 'Activities'

   def __str__(self):
      return str(self.activity_ID)