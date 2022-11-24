from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'emp_app/index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'emp_app/show.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])
        add_new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone,
                               dept_id=dept, role_id=role, hire_date=datetime.now())
        add_new_emp.save()
        return HttpResponse('Employee Added Successfully')
    elif request.method == 'GET':
        return render(request, 'emp_app/add.html')
    else:
        return HttpResponse('Employee Exception occured! Employee has not been Added.')


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            employee = Employee.objects.get(id=emp_id)
            employee.delete()
            return HttpResponse('Employee Removed Successfully')
        except:
            return HttpResponse('Please enter a Valid Employee ID')
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'emp_app/remove.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        context = {
            'emps': emps
        }
        return render(request, 'emp_app/show.html', context)

    elif request.method == 'GET':
        return render(request, 'emp_app/filter.html')
    else:
        return HttpResponse('An exception Occured!')
