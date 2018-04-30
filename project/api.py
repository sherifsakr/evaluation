# #from rest_framework.generics import  ListAPIView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import  viewsets
# 
# from .serializers import EmployeeSerializer, EvaluationSerializer
# from .models import Employee, Evaluation
# 
# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
# 
# class EvaluationViewSet(viewsets.ModelViewSet):
#     queryset = Evaluation.objects.all()
#     serializer_class = EvaluationSerializer
#     
#     
# class EmployeeEvaluationViewSet(viewsets.ModelViewSet):
#     queryset = Evaluation.objects.all()
#     serializer_class = EvaluationSerializer
#     
#     