from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_date
from .utils import *
from datetime import date,datetime,timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Sum



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
   total_members= MemberProfile.objects.count()
   active_membership= MemberProfile.objects.filter(membership_end__gte= timezone.now().date()).count()
   total_registration = MemberProfile.objects.filter(joining_date=timezone.now().date()).count() 
   pending_payments= payment.objects.filter(status='PENDING').count()

   return render(request, 'admin_dashboard.html', {
       'total_members':total_members,
       'active_membership':active_membership,
       'total_registration': total_registration,
       'pending_payments': pending_payments,

   })


def logout_view(request):
    logout(request)  # Log out the user and end the session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Redirect to admin login page after logout



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
        # joining_date = request.POST.get('joining_date') or timezone.now().date()
        joining_date = request.POST.get("joining_date")
        if joining_date:
            joining_date = datetime.strptime(joining_date, "%Y-%m-%d").date()
        else:
            joining_date = timezone.now().date()


        plan_id = request.POST.get('plan_id')
        trainer_id = request.POST.get('trainer_id')

        if User.objects.filter(username= username).exists():
            messages.error(request, 'Username already exists. Please choose a different username. ')
            return redirect('admin_member_add')
        

        # user = User.objects.create_user(username=username, password= password, role="MEMBER")
        user = User.objects.create_user(username=username, password=password)
        user.role = "MEMBER"
        user.save(update_fields=['role'])  # ← only saves the role, not other fields

        plan = MembershipPlan.objects.get(id=plan_id) if plan_id else None
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None

        membership_start = joining_date
        membership_end = None
        if plan:
            membership_end = membership_start + relativedelta(
                months=plan.duration_months
            )


        MemberProfile.objects.create(
            user = user,
            full_name = full_name,
            mobile = mobile,
            age = age,
            gender=gender,
            address=address,
            joining_date=joining_date,
            plan=plan,
            trainer=trainer,
            membership_start=membership_start,
            membership_end=membership_end
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


#============ For enquaries===================================================

#==============admin_workout_plan=============================================
@admin_required
def admin_workout_plans_list(request):
    member_id = request.GET.get('member_id')
    workout_plans = WorkoutPlan.objects.select_related('member').all().order_by('-created_at')

        #dropdown ma sabai members haru show garna laie 
    members= MemberProfile.objects.all().order_by('full_name')

    if member_id:
        workout_plans = workout_plans.filter(member__id = member_id)


    return render(request, 'admin_workout_plans_list.html', {
        'workout_plans' : workout_plans, 
        'members' :members, 
        'selected_member_id': member_id} )



@admin_required
def admin_workout_plan_add(request):
    members = MemberProfile.objects.all().order_by('full_name')
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        title= request.POST.get('title')
        description = request.POST.get('description')

        if not member_id or not title or not description:
            messages.error(request, 'Please select a member and enter plan details.')
            return redirect('admin_workout_plan_add')
        
        member = MemberProfile.objects.get(id=member_id)

        WorkoutPlan.objects.create(
            member = member,
            title = title,
            description = description
        )
        messages.success(request, 'workout Plann added successfullly ! ')
        return redirect('admin_workout_plans_list')
    return render(request, 'admin_workout_plan_form.html', {
        'members': members,
        })



@admin_required
def admin_workout_plan_edit(request, plan_id):
    edit_plan = get_object_or_404(WorkoutPlan, id=plan_id)
    # edit_plan= WorkoutPlan.objects.get(id=plan_id)
    members = MemberProfile.objects.all().order_by('full_name')
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        title= request.POST.get('title')
        description = request.POST.get('description')

        if not member_id or not title or not description:
            messages.error(request, 'Please select a member and enter plan details.')
            return redirect('admin_workout_plan_edit', plan_id=plan_id)
        
        member = MemberProfile.objects.get(id=member_id)

        edit_plan.member = member
        edit_plan.title = title
        edit_plan.description = description
        edit_plan.save()

        messages.success(request, 'Workout Plan updated successfully ! ')
        return redirect('admin_workout_plans_list')
    return render(request, 'admin_workout_plan_form.html', {
        'plan': edit_plan,
        'members': members,
        'mode': 'edit'
        })



       



@admin_required
def admin_workout_plan_delete(request, plan_id):
    plan = WorkoutPlan.objects.get(id=plan_id)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Workout plan deleted successfully! ")
        return redirect('admin_workout_plans_list')
    return redirect('admin_workout_plans_list')


#===============================================================================================

@admin_required
def admin_payments_list(request):
    member_id = request.GET.get('member_id')
    status= request.GET.get('status')
    payments = payment.objects.select_related('member','Plan').all().order_by('-payment_date') #latest payment mathi hunx

    if member_id:
        payments= payments.filter(member__id=member_id)
    if status in ['PENDING', 'PAID']:
        payments = payments.filter(status=status)

#members ko all data  memberprofile ko table bata nikalne
    members = MemberProfile.objects.all().order_by("full_name")

    return render(request,'admin_payments_list.html', {
        'payments':payments, 
        'members':members,
        'selected_member_id': member_id,
        'selected_status':status,
        })




@admin_required
def admin_payment_add(request):
    members = MemberProfile.objects.all().order_by('full_name')
    plans= MembershipPlan.objects.all().order_by('duration_months')
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        plan_id = request.POST.get('plan_id')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date') or timezone.now().date()
        mode= request.POST.get('mode')
        status = request.POST.get('status')
        notes = request.POST.get('notes')

        set_membership = request.POST.get('set_membership')  #checkbox to set member
        membership_start = request.POST.get('membership_start')

        if not member_id or not plan_id or not amount or not status:
            messages.error(request, 'Please fill in all required fields. ')
            return redirect('admin_payment_add ')
        
        member = MemberProfile.objects.get(id= member_id)
        plan = MembershipPlan.objects.get(id=plan_id)

        #checking over_payment 
        if plan and plan.fees:
            total_paid = payment.objects.filter(
                member = member, Plan = plan, status = 'PAID'
            ).aggregate(total=models.Sum('amount') )['total'] or 0
            if float(total_paid) + float(amount) > float(plan.fees):
                remaining_amount = float(plan.fees) - float(total_paid)
                messages.error(request, f'Total paid amount exceeds the plan fee of {plan.fees}.Remaining amount: {remaining_amount}. Please check the amount.')
                return redirect ('admin_payment_add')


        payment.objects.create(
            member = member,
            Plan = plan,
            amount = amount,
            status = status,
            mode = mode,
            payment_date=payment_date,
            notes=notes
        )
        #check box tik lage ko x ki naie check garne 
        if set_membership == 'on' and plan and membership_start:
            try:
                member_start = timezone.datetime.strptime(membership_start, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid membership start date format. Please use YYY-MM-DD.')
                return redirect('admin_payment_add')
            member.plan = plan
            member.membership_start = member_start
            member.membership_end = member_start + timezone.timedelta(days=plan.duration_months*30)
           
            member.save()

        messages.success(request, 'Payment recorded successfully! ')
        return redirect ('admin_payments_list')
    return render(request, 'admin_payment_form.html', {'members':members, 'plans': plans})

        



        

#=====================================================================================

def members_login_view(request):
    # Similar to admin_login_view but checks for MEMBER role
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

#user le de ko username and password database ma exist gar x ki naie vane r check gar x if x vane user laie return gar x 
#if x en vane non return gar x 
        user = authenticate(request, username=username, password=password)

#if user x vane then check gar x member user ho ki naie if yes then login success hun x else invalid
        if user is not None and getattr(user, 'role', None) == 'MEMBER':  #user model vitra role attribute x ki naei or user is member or not
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('member_dashboard') #member dashboard ma redirect hun x after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'members_login.html')



def member_required(view_function):
    # Decorator for member login 
    #user aunthenticte x ki naie tyo check gar x then user ko role k ho tyo check gar x if member ho vane access pau x 

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None)!= "MEMBER":
            messages.error(request, "You must me an member to access this page.")
            return redirect('member_login')
        return view_function(request, *args, **kwargs)
    return wrapper



@member_required
def member_dashboard_view(request):
    return render (request, 'member_dashboard.html')


@member_required
def member_attendance(request):
    member_profile =MemberProfile.objects.get(user=request.user)
    attendances= Attendance.objects.filter(member=member_profile).order_by('-date')
    return render(request, 'member_attendance.html',{'attendances': attendances})


@member_required
def member_membership(request):
    member= request.user.member_profile
    
    days_remaining= None
    total_paid=0
    remaining_amount= None
    membership_status = "No Membership"

    if member.membership_end:
        days_remaining=(member.membership_end - timezone.now().date()).days
        if days_remaining <= 0:
            days_remaining = 0
            membership_status= "Membership Ended"
        else:
            membership_status = "Active"

    if member.plan:
        aggrigate= payment.objects.filter(
            member= member,
            Plan= member.plan,
            status = 'PAID'
        ).aggregate(total= Sum('amount'))

        total_paid = aggrigate['total'] or 0

        if member.plan.fees:
            remaining_amount= float(member.plan.fees) - float(total_paid)
    
    context ={
        'member' : member,
        'membership_status': membership_status,
        'days_remaining': days_remaining,
        'total_paid' : total_paid,
        'remaining_amount': remaining_amount
    }
    return render(request, 'member_membership.html', context)



