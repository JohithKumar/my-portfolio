from .models import *
from .serializers import *
from courses.models import Course, Lecture
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(student_id=request.user).select_related('course_id')
    data = []
    for en in enrollments:
        total_lectures = Lecture.objects.filter(module_id__course_id=en.course_id).count()
        completed_lectures = LectureProgress.objects.filter(enrollment_id=en, completed=True).count()
        data.append({
            "id": en.id,
            "course": {
                "id": en.course_id.id,
                "title": en.course_id.title,
                "description": en.course_id.description,
                "thumbnail_url": en.course_id.thumbnail_url,
            },
            "status": en.status,
            "total_lectures": total_lectures,
            "completed_lectures": completed_lectures
        })
    return Response(data)

@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    if request.method == 'GET':
        data = Enrollment.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(data, request)
        serializer = EnrollmentSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=400)
        
        # Check if already enrolled
        if Enrollment.objects.filter(student_id=request.user, course_id_id=course_id).exists():
            return Response({'error': 'Already enrolled'}, status=400)
            
        serializer = EnrollmentSerializer(data={
            'student_id': request.user.id,
            'course_id': course_id,
            'status': 'active'
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def enrollment_detail(request, id):
    try:
        obj = Enrollment.objects.get(id=id)
    except:
        return Response({'error': 'Enrollment not found'}, status=404)
    if request.method == 'GET':
        return Response(EnrollmentSerializer(obj).data)
    if request.method == 'PUT':
        serializer = EnrollmentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = EnrollmentSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lectureprogress_list(request):
    if request.method == 'GET':
        data = LectureProgress.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(data, request)
        serializer = LectureProgressSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = LectureProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lectureprogress_detail(request, id):
    try:
        obj = LectureProgress.objects.get(id=id)
    except:
        return Response({'error': 'Progress not found'}, status=404)
    if request.method == 'GET':
        return Response(LectureProgressSerializer(obj).data)
    if request.method == 'PUT':
        serializer = LectureProgressSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = LectureProgressSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lecture_completed(request, lecture_id):
    try:
        lecture = Lecture.objects.get(id=lecture_id)
        enrollment = Enrollment.objects.get(student_id=request.user, course_id=lecture.module_id.course_id)
        
        progress, created = LectureProgress.objects.get_or_create(
            enrollment_id=enrollment,
            lecture_id=lecture,
            defaults={'completed': True}
        )
        
        if not created:
            progress.completed = not progress.completed
            progress.save()
            
        return Response({
            'status': 'success',
            'completed': progress.completed,
            'lecture_id': lecture_id
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)