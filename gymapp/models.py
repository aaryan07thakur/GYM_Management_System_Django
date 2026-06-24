from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  # Import timezone to set default value for date fields
from django.conf import settings   # Import settings to access the custom user model

# Create your models here.

#user model ma role field add gareko, jasma admin ra member ko role define gareko cha.
class User(AbstractUser):  #username, password, email, first_name, last_name

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
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
    


#trainer model ma name, mobile, specialization, shift_timing, experience_years field haru cha.

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)   # Contact information for the trainer
    specialization = models.CharField(max_length=200)
    shift_timing = models.CharField(max_length=100)  # The working hours or shift timing of the trainer
    experience_years = models.PositiveIntegerField()  # Number of years of experience
      

    def __str__(self):
        return f"{self.name} - {self.specialization} - {self.shift_timing} - {self.experience_years} years"
    


#member profile model 
class MemberProfile(models.Model):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other')
    )
    user = models.OneToOneField(
         settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  # Delete profile if user is deleted 
        related_name='member_profile'  # This allows you to access the MemberProfile from the User model using user.member_profile
    )
    
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    mobile = models.CharField(max_length=15)  # Contact information for the member
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(blank=True)
    joining_date = models.DateField(default=timezone.now)  # Set default value to current date
    plan = models.ForeignKey(
        MembershipPlan, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  #if plan delete garne bhaye, member profile ma null value rakhne
        related_name = 'members') # This allows you to access all members associated with a specific 
                                #membership plan using membership_plan.members.all()
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, null=True, blank=True)  #if trainer delete garne bhaye, member profile ma null value rakhne
    related_name = 'members' # This allows you to access all members associated with a specific trainer using trainer.members.all() 

    membership_start= models.DateField(null=True, blank=True)  #date when the membership starts
    membership_end = models.DateField(null=True, blank=True)  #date when the membership ends



    def __str__(self):
        return f"{self.full_name} - {self.user.username}"
    




#5 fields in equipment model: name, quantity, purchase_date, condition, and description.
class Equipment(models.Model):
    name = models.CharField(max_length=100) #e.g 'Treadmill', 'Dumbbells', 'Bench Press', etc.
    units = models.PositiveIntegerField(default=1) #e.g 5 treadmills , 10 dumbbells, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2) # The price of the equipment, eg 500.32
    purchase_date = models.DateField(default=timezone.now)  # The date when the equipment was purchased, defaulting to the current date
    is_active = models.BooleanField(default=True)  # Indicates if the equipment is currently in use
   

    def __str__(self):
        return f"{self.name} - (Units: {self.units})"
    



#payment model yesma 7 fields hun x

class payment(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('CASH', 'Cash'),
        ('ONLINE', 'Online'),
    )
    PAYMENT_STATUS_CHOICES = {
        ('PAID', 'Paid'),
        ('PENDING', 'Pending')
    }


    member = models.ForeignKey(MemberProfile,
                               on_delete=models.CASCADE, #if member profile delete garne bhaye, payment record pani delete garne
                               related_name = 'payments' #Access payments via member.payments
                               )
    Plan= models.ForeignKey(MembershipPlan,
                            on_delete=models.SET_NULL, #if membership plan delete garne bhaye, payment record ma null value rakhne
                            null=True, blank=True,
                            related_name = 'payments' #Access payments via plan.payments
                            )
    amount = models.DecimalField(max_digits=10, decimal_places =2) # The amount paid by the member
    payment_date = models.DateField(default= timezone.now) # The date when the payment was made, defaulting to the current date
    mode = models.CharField(max_length= 50, choices=PAYMENT_MODE_CHOICES) #e.g 'Cash', 'Bank Transfer', etc.
    status = models.CharField(max_length = 50, choices=PAYMENT_STATUS_CHOICES, default= 'PENDING') #e.g 'Paid', 'Pending', etc.
    notes= models.TextField(blank=True )# 


    def __str__(self):
        return f"payment of ${self.amount} by {self.member.full_name} on {self.payment_date}"
    


#attendance model with 3 fields

class Attendance(models.Model):
    member = models.ForeignKey(
        MemberProfile, 
        on_delete=models.CASCADE, #if member profile delete garne bhaye, attendance record pani delete garne
        related_name='attendances'  # Access attendance records via member.attendance_records
        )
    date = models.DateField(default=timezone.now)  # The date of attendance, defaulting to the current date
    time_in = models.TimeField(null=True, blank=True)  # The time when the member checked in

    class Meta:
        unique_together = ('member', 'date') #Ensure one attendance record per member per day


    def __str__(self):
        return f"{self.member.full_name} - {self.date} - {self.time_in}"
                               


#enquary model with 6 fields

class Enquiry(models.Model):
    ENQUIRY_STATUS_CHOICES = (
        ('NEW', 'New'),
        ('INPROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    name = models.CharField(max_length=100) # The name of the person making the enquiry
    email = models.EmailField() # The email address of the person making the enquiry
    mobile = models.CharField(max_length=15) # The mobile number of the person making the enquiry
    message = models.TextField() # The message or content of the enquiry
    created_at = models.DateTimeField(auto_now_add=True) # The date and time when the enquiry was created, automatically set to the current date and time when the record is created
    status = models.CharField(max_length=20, choices=ENQUIRY_STATUS_CHOICES, default='NEW') # The status of the enquiry, with choices for 'New', 'In


    def __str__(self):
        return f"Enquiry from {self.name} - {self.email} - {self.mobile} - Status: {self.status}"






#workout plan model with 4 fields

class WorkoutPlan(models.Model):
    member = models.ForeignKey(
        MemberProfile, 
        on_delete=models.CASCADE, #if member profile delete garne bhaye, workout plan record pani delete garne
        related_name='workout_plans'  # Access workout plans via member.workout_plans
        )
    title = models.CharField(max_length=100) # The Title of the workout plan
    description = models.TextField(blank=True) # A description of the workout plan
    created_at = models.DateTimeField(auto_now_add=True) # The date and time when the workout plan was created, automatically set to the current date and time when the record is created

    def __str__(self):
        return f"{self.title} - Created at: {self.created_at}"




#feedback model with 3 fields

class Feedback(models.Model):
    member = models.ForeignKey(
        MemberProfile, 
        on_delete=models.CASCADE, #if member profile delete garne bhaye, feedback record pani delete garne
        related_name='feedbacks'  # Access feedback records via member.feedbacks
        )
    message = models.TextField() # feedback message provided by the member
    created_at = models.DateTimeField(auto_now_add=True) # The date and time when the feedback was created, automatically set to the current date and time when the record is created


    def __str__(self):
        return f"Feedback from {self.member.full_name} - Created at: {self.created_at}"




