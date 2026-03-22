from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

#custom user model lai admin ma register garna ko lagi, UserAdmin class banayeko, 
# jasma role field add gareko cha. Yo class lai admin.site.register() function ma use 
# gareko cha, jasle custom user model lai admin interface ma properly display garna madat garcha.
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),  # Add the 'role' field to the user admin interface
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')  # Display the role in the user list view
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')  # Add filters for role, staff status, and active status in the user list view



class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'mobile', 'plan', 'joining_date')  # Display user, membership plan, and join date in the member profile list view
    search_fields = ('full_name', 'user__username', 'mobile')  # Add search fields for membership plan and join date in the member profile list view
    list_filter = ('plan', 'joining_date')  # Add filters for membership plan and join date in the member profile list view


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'status', 'created_at')  # Display name, email, mobile, status, and created date in the enquiry list view
    search_fields = ('name', 'email', 'mobile')  # Add search fields for name, email, and mobile in the enquiry list view
    list_filter = ('status', 'created_at')  # Add filters for status and created date in the enquiry list view

admin.site.register(User, UserAdmin) # Register the custom User model with the custom UserAdmin to include the role field in the admin interface
admin.site.register(MembershipPlan)
admin.site.register(Trainer)
admin.site.register(Enquiry, EnquiryAdmin)  
admin.site.register(WorkoutPlan)
admin.site.register(Equipment)
admin.site.register(Attendance)
admin.site.register(Feedback)
admin.site.register(payment)
admin.site.register(MemberProfile, MemberProfileAdmin)  # Register the MemberProfile model with the custom MemberProfileAdmin to include additional fields and filters in the admin interface



