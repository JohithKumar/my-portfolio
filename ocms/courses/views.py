from .models import *
from .serializers import *
from enrollments.models import Enrollment, LectureProgress
from reviews.models import Review
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        data = Category.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated = paginator.paginate_queryset(data, request)
        serializer = CategorySerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def category_detail(request, id):
    try:
        obj = Category.objects.get(id=id)
    except:
        return Response({'error': 'Category not found'}, status=404)
    if request.method == 'GET':
        return Response(CategorySerializer(obj).data)
    if request.method == 'PUT':
        serializer = CategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = CategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        data = Course.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated = paginator.paginate_queryset(data, request)
        serializer = CourseSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def course_detail(request, id):
    try:
        obj = Course.objects.get(id=id)
    except:
        return Response({'error': 'Course not found'}, status=404)
    if request.method == 'GET':
        return Response(CourseSerializer(obj).data)
    if request.method == 'PUT':
        serializer = CourseSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = CourseSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_detail_full(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
        
    is_enrolled = Enrollment.objects.filter(student_id=request.user, course_id=course).exists()
    
    modules = Module.objects.filter(course_id=course).order_by('order')
    modules_data = []
    for mod in modules:
        lectures = Lecture.objects.filter(module_id=mod).order_by('order')
        lectures_data = []
        for l in lectures:
            completed = False
            if is_enrolled:
                completed = LectureProgress.objects.filter(
                    enrollment_id__student_id=request.user, 
                    lecture_id=l, 
                    completed=True
                ).exists()
            
            lectures_data.append({
                "id": l.id, 
                "title": l.title, 
                "video_url": l.video_url, 
                "resources_url": l.resources_url,
                "duration": l.duration, 
                "type": l.lecture_type,
                "completed": completed
            })
            
        modules_data.append({
            "id": mod.id,
            "title": mod.title,
            "order": mod.order,
            "lectures": lectures_data
        })
    
    reviews = Review.objects.filter(course_id=course).order_by('-created_at')
    reviews_data = [{
        "id": r.id, 
        "student": r.student_id.full_name or r.student_id.username, 
        "rating": r.rating, 
        "comment": r.comment,
        "date": r.created_at.strftime("%Y-%m-%d") if r.created_at else ""
    } for r in reviews]

    course_data = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor_id.full_name,
        "price": course.price,
        "level": course.level,
        "thumbnail_url": course.thumbnail_url,
        "modules": modules_data if is_enrolled else [],
        "is_enrolled": is_enrolled,
        "reviews": reviews_data
    }
    return Response(course_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_enroll(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
        
    enrollment, created = Enrollment.objects.get_or_create(student_id=request.user, course_id=course, defaults={'status': 'active'})
    return Response({'success': 'Enrolled successfully', 'created': created})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_add_review(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
        
    rating = request.data.get('rating', 5)
    comment = request.data.get('comment', '')
    
    review = Review.objects.create(
        student_id=request.user,
        course_id=course,
        rating=rating,
        comment=comment
    )
    return Response({'success': 'Review added successfully', 'review_id': review.id})

@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def module_list(request):
    if request.method == 'GET':
        data = Module.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        paginated = paginator.paginate_queryset(data, request)
        serializer = ModuleSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def module_detail(request, id):
    try:
        obj = Module.objects.get(id=id)
    except:
        return Response({'error': 'Module not found'}, status=404)
    if request.method == 'GET':
        return Response(ModuleSerializer(obj).data)
    if request.method == 'PUT':
        serializer = ModuleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = ModuleSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'POST'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lecture_list(request):
    if request.method == 'GET':
        data = Lecture.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(data, request)
        serializer = LectureSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def lecture_detail(request, id):
    try:
        obj = Lecture.objects.get(id=id)
    except:
        return Response({'error': 'Lecture not found'}, status=404)
    if request.method == 'GET':
        return Response(LectureSerializer(obj).data)
    if request.method == 'PUT':
        serializer = LectureSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        obj.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = LectureSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)