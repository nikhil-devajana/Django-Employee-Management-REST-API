from django.http import HttpResponse
from .models import Employee
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def employee_list_view(request):

    if request.method=='GET':
        employees=Employee.objects.all()
        employee_list=[]
        for employee in employees:
            emp_dict={
                    'name':employee.name,
                    'email':employee.email,
                    'salary':employee.salary,
                    'address':employee.address,
                    'role':employee.role
            }
            employee_list.append(emp_dict)
        response=json.dumps(employee_list)
        return HttpResponse(response,content_type='application/json',status=200)

    if request.method=='POST':
        request=json.loads(request.body)
        employee=Employee.objects.create(**request)
        data={
            'Message':'Employee Created Successfully',
            'data':{
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'salary':employee.salary,
                'address':employee.address,
                'role':employee.role
            }
        }
        response=json.dumps(data)
        return HttpResponse(response,content_type='application/json',status=201)

    error={
        'Message':"Only 'GET' & 'POST' can be used"
    }
    return HttpResponse(error,content_type='applicatio/json',status=404)

@csrf_exempt
def employee_details_view(request,employee_id):
    try:
        employee=Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        error={
            'Message':'Employee does not Exits'
        }
        response=json.dumps(error)
        return HttpResponse(response,content_type='application/json',status=404)

    if request.method=='GET':
        data={
            'Message':'Fetched individual Employee Successfully',
                'data':{
                    'id':employee.id,
                    'name':employee.name,
                    'email':employee.email,
                    'salary':employee.salary,
                    'address':employee.address,
                    'role':employee.role
                }
        }
        response=json.dumps(data)
        return HttpResponse(response,content_type='application/json',status=200)

    if request.method=='PUT':
        request_data=json.loads(request.body)

        fields=['name','email','address','role','salary']
        missingfield_list=[]
        for field in fields:
            if field not in request_data:
                missingfield_list.append(field)
        if missingfield_list:
            error={
                'Message':'Missing Mandatory Fields',
                'missing_field':missingfield_list
            }
            response=json.dumps(error)
            return HttpResponse(response,content_type='application/json',status=404)
        employee.name=request_data['name']
        employee.salary=request_data['salary']
        employee.email=request_data['email']
        employee.address=request_data['address']
        employee.role=request_data['role']
        employee.save()

        data={
           'Message':'Employee detail Replaced',
           'data':{
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'salary':employee.salary,
                'address':employee.address,
                'role':employee.role
                }
            }
        response=json.dumps(data)
        return HttpResponse(response,content_type='application/json',status=200)

    if request.method=='PATCH':
        request_data=json.loads(request.body)

        employee.name=request_data.get('name',employee.name)
        employee.salary=request_data.get('salary',employee.salary)
        employee.role=request_data.get('role',employee.role)
        employee.address=request_data.get('address',employee.address)
        employee.email=request_data.get('email',employee.email)
        employee.save()
        data={
            'Message':'Employee details Modified',
            'data':{
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'salary':employee.salary,
                'address':employee.address,
                'role':employee.role
                }
            }
        response=json.dumps(data)
        return HttpResponse(response,content_type='application/json',status=200)

    if request.method=='DELETE':
        employee.delete()
        data={
            'Message':'Employee deleted',
            'data':{
                'id':employee.id,
                'name':employee.name,
                'email':employee.email,
                'salary':employee.salary,
                'address':employee.address,
                'role':employee.role
                }
            }
        response=json.dumps(data)
        return HttpResponse(response,content_type='application/json',status=200)
    error={
        'Message':"Only 'GET' & 'POST' can be used"
    }
    return HttpResponse(error,content_type='applicatio/json',status=404)