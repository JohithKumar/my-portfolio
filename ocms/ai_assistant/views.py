from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import ChatMessage
import random

@api_view(['POST'])
@permission_classes([AllowAny]) # Allow any for now to facilitate testing, will restrict if needed
def chat_response(request):
    user_message = request.data.get('message', '')
    if not user_message:
        return Response({'response': "I'm here to help! What's your question?"})

    # Simple rule-based mock responses for the AI Assistant
    responses = [
        f"That's a great question about '{user_message}'! As your OCMS.IO assistant, I'd recommend checking the 'Technical Architecture' section for more details.",
        "I'm analyzing your request. Based on our curriculum, this topic is covered in Module 3 of the Full-Stack Web Development course.",
        "Welcome to OCMS! I can help you with course enrollments, lecture progress, or technical support. What would you like to explore first?",
        "Progress is key! Don't forget that you can track your curriculum completion directly in the course player.",
        "Our instructors recommend spending at least 30 minutes a day on labs to solidify your learning."
    ]
    
    selected_response = random.choice(responses)
    
    # Store the message if user is authenticated
    user_obj = request.user if request.user.is_authenticated else None
    ChatMessage.objects.create(user=user_obj, message=user_message, response=selected_response)

    return Response({
        'response': selected_response,
        'status': 'success'
    })
