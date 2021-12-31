from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TblSurvey, TblQuestion, TblAnswerQuestions, TblCompletedSurvey
from .serializers import SurveySerializer, QuestionSerializer, CompletedSurveySerializer
# AnswerQuestionsSerializer, AnswerQuestionsGETSerializer, \
    # CompletedSurveySerializer
from rest_framework import status


class SurveyView(APIView):
    """DONE"""
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            survey = TblSurvey.objects.get(id=pk)
            serializer = SurveySerializer(survey)
        else:
            survey = TblSurvey.objects.all()
            serializer = SurveySerializer(survey, many=True)
        return Response({"results": serializer.data})


class SurveyAnswersView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        answers = TblCompletedSurvey.objects.filter(id=pk)
        serializer = CompletedSurveySerializer(answers, many=True)
        return Response({"results": serializer.data})
#
#
# class QuestionsView(APIView):
#
#     def post(self, request):
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
class ToAnswerView(APIView):
    """DONE"""
    def post(self, request):
        serializer = CompletedSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
