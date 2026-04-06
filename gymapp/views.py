from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_date
from .utils import *
from datetime import date



# Create your views here.



def home(request):
    '''simple home page + contact/enquiry form'''
    if request.method == 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        mobile= request.POST.get('mobile')
        message= request.POST.get('message')

# validate the form data and save the enquiry to the database
        if name and email and mobile and message:
            Enquiry.objects.create(name=name, email=email, mobile=mobile, message=message)
            messages.success(request, 'Your enquiry has been submitted successfully.')
            return redirect('home') # Redirect to the home page after successful submission
        else:
            messages.error(request, 'Please fill in all fields.')
                
    return render(request, 'home.html')




def about(request):
    return render(request, 'about.html')



def admin_login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

# authenticate function le check garxa ki username ra password sahi cha ki nai database ma , ani user object return garxa
        user = authenticate(request, username=username, password=password) 

        if user is not None and getattr(user, 'role', None) == 'ADMIN':  # Check if the user is authenticated and has the admin role
            login(request, user) # Login the user and create a session
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')  # Redirect to admin dashboard upon successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')


#decorator 
def admin_required(view_func):
    '''Decorator to check if the user is authenticated and has the admin role  '''

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'ADMIN':
            messages.error(request, 'You must be an admin to access this page.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper




@admin_required
def admin_dashboard_view(request):
   return render(request, 'admin_dashboard.html')


def logout_view(request):
    logout(request)  # Log out the user and end the session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')  # Redirect to admin login page after logout



@admin_required
def admin_plans_list(request):
    plans= MembershipPlan.objects.all().order_by("duration_months")
    return render(request, 'admin_plans_list.html', {'plans': plans})


@admin_required
def admin_plan_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        duration_months = request.POST.get ('duration_months')
        fees = request.POST.get('fees')
        description = request.POST.get('description')

        if name and duration_months and fees:
            MembershipPlan.objects.create(
                name=name,
                duration_months=duration_months,
                fees=fees,
                description=description
            )
            messages.success(request, 'Membership plan added successfully!! ')
            return redirect('admin_plans_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'admin_plan_form.html', {'mode': 'add'})



@admin_required
def admin_plan_edit(request,plan_id):
    plan= MembershipPlan.objects.get(id=plan_id)
    if request.method == "POST":
        name= request.POST.get('name')
        duration_months = request.POST.get('duration_months')
        fee= request.POST.get('fees')
        description = request.POST.get('description')

        if name and duration_months and fee:
            plan.name = name
            plan.duration_months = duration_months
            plan.fees = fee
            plan.description = description
            plan.save()
            messages.success(request, "Membership plan updated successfully! ")
            return redirect('admin_plans_list')
        else:
            messages.error(request, "Please fill in all required fields. ")
    return render(request, 'admin_plan_form.html', {'plan': plan, 'mode': 'edit' })



@admin_required
def admin_plan_delete(request,plan_id):
    plan=MembershipPlan.objects.get(id=plan_id)
    if request.method == "POST":
        plan.delete()
        messages.success(request, 'Membership plan deleted successfully ! ')
        return redirect ('admin_plans_list')
    return redirect(request, 'admin_plans_list')




@admin_required
def admin_trainers_list(request):
    trainers= Trainer.objects.all().order_by("name")
    return render(request, 'admin_trainers_list.html', {'trainers': trainers})



@admin_required
def admin_trainer_add(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        specialization= request.POST.get('specialization')
        shift_timing = request.POST.get('shift_timing')
        experience_years = request.POST.get('experience_years')

        if name and mobile and specialization and shift_timing and experience_years:
            Trainer.objects.create(
                name=name,
                mobile=mobile,
                specialization=specialization,
                shift_timing=shift_timing,
                experience_years=experience_years
            )
            messages.success(request, 'New Trainer added successfully !!')
            return redirect('admin_trainers_list')
        else:
            messages.error(request, 'please Fill in all required field!!')
    return render(request, 'admin_trainer_form.html', {'mode': 'add'})
        


@admin_required
def admin_trainer_edit(request,trainer_id):
    trainer= Trainer.objects.get(id=trainer_id)
    if request.method == "POST":
        name= request.POST.get('name')
        mobile = request.POST.get('mobile')
        specialization= request.POST.get('specialization')
        shift_timing = request.POST.get('shift_timing')
        experience_years = request.POST.get('experience_years')

        if name and mobile and specialization and shift_timing and experience_years:
            trainer.name = name
            trainer.mobile = mobile
            trainer.specialization = specialization
            trainer.shift_timing = shift_timing
            trainer.experience_years = experience_years

            trainer.save()
            messages.success(request, "Trainer updated successfully! ")
            return redirect('admin_trainers_list')
        else:
            messages.error(request, "Please fill in all required fields. ")
    return render(request, 'admin_trainer_form.html', {'trainer': trainer, 'mode': 'edit' })




@admin_required
def admin_trainer_delete(request,trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    if request.method == 'POST':
        trainer.delete()
        messages.success(request, 'Trainer deleted successfully !')
        return redirect('admin_trainers_list')
    return redirect('admin_trainers_list')




@admin_required
def admin_members_list(request):
    search=request.GET.get('search','').strip()

    members= MemberProfile.objects.all().select_related('user', 'plan')

    if search:
        members = members.filter(full_name__icontains=search)  

    return render(request, 'admin_members_list.html', {'members': members,'search':search})



@admin_required
def admin_member_add(request):
    plans = MembershipPlan.objects.all().order_by('duration_months') #plans ko sabai data layau ne
    Trainers = Trainer.objects.all().order_by('name')  #sabai trainer laei layau ne 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        age= request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        joining_date = request.POST.get('joining_date') or timezone.now().date()

        plan_id = request.POST.get('plan_id')
        trainer_id = request.POST.get('trainer_id')

        if User.objects.filter(username= username).exists():
            messages.error(request, 'Username already exists. Please choose a different username. ')
            return redirect('admin_member_add')
        

        user = User.objects.create_user(username=username, password= password, role="MEMBER")

        plan = MembershipPlan.objects.get(id=plan_id) if plan_id else None
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None

        MemberProfile.objects.create(
            user = user,
            full_name = full_name,
            mobile = mobile,
            age = age,
            gender=gender,
            address=address,
            joining_date=joining_date,
            plan=plan,
            trainer=trainer
        )
        messages.success(request, 'Member added successfully! ')
        return redirect('admin_members_list')
    return render(request, 'admin_member_form.html', 
                {'plans': plans, 'trainers': Trainers,'mode':'ADD' })



@admin_required
def admin_member_edit(request,member_id):
   member= MemberProfile.objects.get(id= member_id)
   plans = MembershipPlan.objects.all().order_by('duration_months')
   trainers= Trainer.objects.all().order_by('name')
   if request.method == 'POST':
       full_name=request.POST.get('full_name')
       mobile = request.POST.get('mobile')
       age= request.POST.get('age')
       address=request.POST.get('address')
       gender= request.POST.get('gender')
       joining_date = request.POST.get('join_date') or member.joining_date
       plan_id= request.POST.get('plan_id')
       trainer_id= request.POST.get('trainer_id')

       plan= MembershipPlan.objects.get(id=plan_id) if plan_id else None
       trainer= Trainer.objects.get(id= trainer_id) if trainer_id else None

       member.full_name= full_name
       member.mobile = mobile
       member.age = age
       member.gender = gender
       member.address = address
       member.joining_date = joining_date
       member.plan = plan
       member.trainer = trainer
       member.save()
       messages.success(request, 'Member updated successfully ! ')
       return redirect('admin_members_list')
   return render(request, 'admin_member_form.html',{
       'member' : member, 'plans': plans, 'trainers': trainers, 'mode': 'edit'
   } )




@admin_required
def admin_member_delete(request, member_id):
    member = MemberProfile.objects.get(id=member_id)
    if request.method == 'POST':
        user= member.user #get the associated user object
        member.delete() 
        user.delete()
        messages.success(request, 'Member deleted successfully! ')
        return redirect('admin_members_list')
    return redirect('admin_members_list')

#==========================================================================================================================

@admin_required
def admin_attendance_list(request):
    today = timezone.now().date()

    date_str = request.GET.get('date')

    if date_str:
        date=parse_date(date_str)
    else:
        date=today
    
    attendances = Attendance.objects.all().select_related('member')

    if date:
        attendances = attendances.filter(date=date)

    members = MemberProfile.objects.all().order_by("full_name") 

    member_id = request.GET.get('member_id')
    if member_id:
        attendances = attendances.filter(member_id=member_id)

    return render(request,'admin_attendance_list.html', 
                {'attendances': attendances, 
                 'members': members, 
                 'selected_date':date,
                 'selected_member_id': member_id})

@admin_required
def admin_attendance_add(request):
    members = MemberProfile.objects.all().order_by("full_name")

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        date_str = request.POST.get('date')
        time_in = request.POST.get('time_in')

        if not member_id:
            messages.error(request, "Please select a member.")
            return redirect('admin_attendance_add')

        if not time_in:
            messages.error(request, "Time In is required.")
            return redirect('admin_attendance_add')

        # validate date
        att_date = validate_date(request, date_str, "Attendance Date")
        if not att_date:
            return redirect('admin_attendance_add')

        member = MemberProfile.objects.get(id=member_id)

        attendance, created = Attendance.objects.get_or_create(
            member=member, date=att_date  # validated date use
        )
        attendance.time_in = time_in
        attendance.save()

        if created:
            messages.info(request, 'Attendance recorded successfully!')
        else:
            messages.success(request, 'Attendance updated successfully!')

    return render(request, 'admin_attendance_form.html', {
        'members': members,
        'today': date.today(),
    })

#=============================================================================================================


@admin_required
def admin_equipment_list(request):
    equipment = Equipment.objects.all().order_by("name")
    return render(request, 'admin_equipment_list.html', {
        'equipments': equipment
    })



@admin_required
def admin_equipment_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        units = request.POST.get('units')
        price = request.POST.get('price')
        purchase_date = request.POST.get('purchase_date') or timezone.now().date()

        purchase_date_obj= validate_date(request, purchase_date)
        if not purchase_date_obj:
            return redirect ('admin_equipment_add')

#required field check gar ne
        if not name or not units or not price:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('admin_equipment_add')

#equiment create garne with validated date
        Equipment.objects.create(
            name=name,
            units=units,
            price=price,
            purchase_date=purchase_date_obj,

        )
        messages.success(request, "Equipment added successfully ! ")
        return redirect("admin_equipment_list")
    
    return render (request, 'admin_equipment_form.html', {
        'mode':'add',
        'today': date.today(),
        })



@admin_required
def admin_equipment_edit(request,equipment_id):
    equipment= get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        name=request.POST.get('name')
        units = request.POST.get('units')
        price= request.POST.get('price')
        purchase_date=request.POST.get('purchase_date')

        purchase_date_obj= validate_date(request, purchase_date)
        if not purchase_date_obj:
            return redirect ('admin_equipment_edit')
        
        if not name or not units or not price:
            messages.error(request, "All fields are required ! ")
            return redirect('admin_equipment_edit', equipment_id=equipment_id)
        try:
            equipment.name= name
            equipment.units = units
            equipment.price = price
            equipment.purchase_date = purchase_date
            equipment.save()

            messages.success(request, 'equipment updated successfully ! ')
            return redirect('admin_equipment_list')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('admin_equipment_edit', equipment_id=equipment_id)
        
    return render(request, 'admin_equipment_form.html',{
        'equipment' : equipment, 
        'mode': 'edit',
        'today': date.today(),
    })



@admin_required
def admin_equipment_delete(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    if request.method == 'POST':
        equipment.delete() 
        messages.success(request, 'equipment deleted successfully! ')
        return redirect('admin_equipment_list')
    return redirect('admin_equipment_list')



#============ For enquaries===================================================
@admin_required
def admin_enquiries_list(request):
    enquiries= Enquiry.objects.all().order_by('-created_at')
    return render(request, 'admin_enquiries_list.html', {'enquiries': enquiries})



@admin_required
def admin_enquiry_update_status(request, enquiry_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        enquiry = Enquiry.objects.get(id= enquiry_id)
        if status in ['NEW', 'SEEN', "RESOLVED"]:
            enquiry.status = status
            enquiry.save()
            messages.success(request, 'Enquiry status updated')
    return redirect('admin_enquiries_list')



#=====================================================================================
def members_login_view(request):
    # Similar to admin_login_view but checks for MEMBER role
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and getattr(user, 'role', None) == 'MEMBER':
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'members_login.html')




