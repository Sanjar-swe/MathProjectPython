from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.models import Question, BotUser, TestAttempt
from apps.serializers import QuestionSerializer, BotUserSerializer, TestAttemptSerializer
from django.db.models import Count, Q
import openpyxl

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['post'], url_path='import-excel')
    def import_excel(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
            
            questions_created = 0
            for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
                # Expected format: Text, Option A, Option B, Option C, Option D, Correct (a/b/c/d)
                if not row[0]: continue
                
                Question.objects.create(
                    text=row[0],
                    option_a=row[1],
                    option_b=row[2],
                    option_c=row[3],
                    option_d=row[4],
                    correct_answer=str(row[5]).lower()
                )
                questions_created += 1
                
            return Response({"message": f"Successfully imported {questions_created} questions"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BotUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

class TestAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestAttempt.objects.all()
    serializer_class = TestAttemptSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total_users = BotUser.objects.count()
        total_attempts = TestAttempt.objects.count()
        top_users = TestAttempt.objects.order_by('-score')[:10]
        
        # Difficult questions: most incorrect answers (where attemptdetail__is_correct=False)
        difficult_questions = Question.objects.annotate(
            incorrect_count=Count('attemptdetail', filter=Q(attemptdetail__is_correct=False))
        ).filter(incorrect_count__gt=0).order_by('-incorrect_count')[:5]
        
        difficult_data = [
            {
                "id": q.id,
                "text": q.text[:50],
                "incorrect_count": q.incorrect_count
            } for q in difficult_questions
        ]
        
        return Response({
            "total_users": total_users,
            "total_attempts": total_attempts,
            "top_users": TestAttemptSerializer(top_users, many=True).data,
            "difficult_questions": difficult_data
        })
