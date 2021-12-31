from rest_framework import serializers
import uuid
from .models import TblSurvey, TblQuestion, TblAnswerOption, TblAnswerQuestions, TblCompletedSurvey, TblParticipant


def is_valid_uuid(value):
    try:
        uuid.UUID(value)

        return True
    except ValueError:
        return False


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblParticipant
        fields = ['full_name']


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField(
            'get_questions', read_only=True
        )

    def get_questions(self, obj):
        questions = TblQuestion.objects.filter(survey=obj).order_by('question_type')
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data

    class Meta:
        model = TblSurvey
        fields = ["id", "survey_name", "survey_description", "questions", "start_time", "finish_time"]


class SurveyAnswersSerializer(SurveySerializer):

    def get_questions(self, obj):
        questions = TblQuestion.objects.filter(survey=obj)
        answer_questions = TblAnswerQuestions.objects.filter(question__in=questions).order_by('question__question_type')
        serializer = AnswerQuestionsSerializer(answer_questions, many=True)
        return serializer.data


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAnswerOption
        fields = ["id", "text"]


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_type = serializers.CharField(max_length=200)
    survey_id = serializers.IntegerField()
    question_text = serializers.CharField(max_length=200)
    answer_options = AnswerOptionSerializer(many=True)


class QuestionWithAnswersSerializer(QuestionSerializer):
    answer_options = None


class AnswerQuestionsSerializer(serializers.ModelSerializer):
    question = QuestionWithAnswersSerializer()
    answers = AnswerOptionSerializer(many=True)

    class Meta:
        model = TblAnswerQuestions
        fields = ["id", "question", "answers"]


class AnswerQuestionsSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = TblAnswerQuestions
        fields = ["id", "question", "answers"]


class CompletedSurveySerializer(serializers.Serializer):
    survey = SurveyAnswersSerializer(read_only=True)
    participant = ParticipantSerializer(read_only=True)
    survey_id = serializers.CharField(max_length=40, write_only=True)
    full_name = serializers.CharField(max_length=20, write_only=True)
    questions = AnswerQuestionsSerializer2(many=True, write_only=True)

    def create(self, validated_data):
        survey = TblSurvey.objects.get(id=validated_data.get('survey_id'))
        questions = validated_data.pop('questions')
        participant = TblParticipant.objects.create(
            full_name=validated_data.get('full_name')
        )
        completed_survey = TblCompletedSurvey.objects.create(
            survey=survey,
            participant=participant
        )

        for answer in questions:
            answer_options = answer.get('answers')
            a = TblAnswerQuestions.objects.create(
                question=answer.get('question'), completed_survey=completed_survey)
            if is_valid_uuid(answer_options[0]):
                a.answers.set(answer_options)
            else:
                answer_option = TblAnswerOption.objects.create(
                    question=answer.get('question'), text=answer.get('answers'))
                a.answers.set(answer_option)
        return questions
