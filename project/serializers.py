# from rest_framework import serializers
# from .models import Employee, Evaluation
# 
# 
# 
# class EmployeeSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         model = Employee
#         #fields = '__all__'  # all model fields will be included
#         fields = ('empname',)
# 
# 
# class EvaluationSerializer(serializers.ModelSerializer):
#     employeeid = EmployeeSerializer(many=False, read_only=True)
# 
#     class Meta:
#         model = Evaluation
#         fields = '__all__'  # all model fields will be included
#         #fields = ('id', 'name', 'employee')
