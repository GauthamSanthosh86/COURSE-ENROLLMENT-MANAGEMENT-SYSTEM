from django.db.models import Model
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from enrollment.models import Enrollment
from enrollment.serializers import EnrollmentSerializer
from django.db import DatabaseError
from django.db.models import Count, Sum, Avg


# Create your views here.

class EnrollmentListCreate(APIView):
    def get(self,request):
        qs=Enrollment.objects.all()
        serializer_instance=EnrollmentSerializer(qs,many=True)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer_instance=EnrollmentSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentRetrieveUpdateDelete(APIView):
    def get(self, request, pk):
        e = get_object_or_404(Enrollment, pk=pk)
        serializer_instance = EnrollmentSerializer(e)
        return Response(serializer_instance.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        e = get_object_or_404(Enrollment, pk=pk)
        serializer_instance = EnrollmentSerializer(instance=e, data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data, status=status.HTTP_200_OK)
        return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        e = get_object_or_404(Enrollment, pk=pk)
        e.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnrollmentPartialUpdate(APIView):
    def patch(self,request,pk):
        e = get_object_or_404(Enrollment, pk=pk)
        serializer_instance=EnrollmentSerializer(instance=e, data=request.data, partial=True)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data, status=status.HTTP_200_OK)
        return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchApi(APIView):
    def get(self,request):
        data=request.query_params.get('search')
        r=Enrollment.objects.filter(Q(status__iexact=data)|Q(student_name__icontains=data)|Q(course_name__icontains=data))
        serializer_instance=EnrollmentSerializer(r,many=True)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)

class EnrollmentSummary(APIView):

    def get(self, request):
        try:
            totals = Enrollment.objects.aggregate(
                total_enrollments=Count('pk'),
                total_fees_collected=Sum('fee'),
                average_fee=Avg('fee'),
            )
            by_status = {
                row['status']: row['count']
                for row in Enrollment.objects.values('status').annotate(count=Count('pk'))
            }
        except DatabaseError as e:
            return Response({'error': f'Database error: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        totals['by_status'] = by_status
        return Response(totals, status=status.HTTP_200_OK)
