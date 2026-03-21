from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  # Import timezone to set default value for date fields
from django.conf import settings   # Import settings to access the custom user model

# Create your models here.

class User(AbstractUser):  #username, password, email, first_name, last_name

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('Member', 'Member'),
    )
  
    role = models.CharField(max_length=20, choices= ROLE_CHOICES, default='MEMBER')

# This method is used to return a string representation of the User object,
#  which includes the username and role. This can be helpful for debugging 
# and displaying user information in the admin interface or other parts of the application.
    def __str__(self):
        return f"{self.username} ({self.role})" 
    


# The Membership model represents different types of gym memberships,
#  each with a name and price. This model can be used to manage the various
# membership options available at the gym, allowing for easy retrieval and display
#  of membership information.

class MembershipPlan(models.Model):  #models.model laie inherit garne
    name = models.CharField(max_length=100)
    duration_months = models.PositiveBigIntegerField()  # Duration of the membership in months
    fees = models.DecimalField(max_digits=10, decimal_places=2) # The price of the membership plan, with up to 10 digits and 2 decimal places for cents.
    description = models.TextField(blank=True, null=True)  # Optional field for additional details about the membership plan




# This method returns a string representation of the MembershipPlan object, including its name, duration in months, and fees. 
# This can be useful for displaying membership plan information in the admin interface or other parts of the application.
    def __str__(self):
        return f"{self.name} - {self.duration_months} months - ${self.fees}"  
    


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField(max_length=10)   # Contact information for the trainer
    specialization = models.CharField(max_length=200)
    shift_timing = models.CharField(max_length=100)  # The working hours or shift timing of the trainer
    experience_years = models.PositiveIntegerField()  # Number of years of experience
      

    def __str__(self):
        return f"{self.name} - {self.specialization} - {self.shift_timing} - {self.experience_years} years"




