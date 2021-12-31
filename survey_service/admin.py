from django.contrib import admin
from .models import TblSurvey, TblParticipant, TblQuestion, TblCompletedSurvey, \
    TblAnswerQuestions, TblAnswerOption


class SurveyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblSurvey._meta.fields]


class TblParticipantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblParticipant._meta.fields]


class TblCompletedSurveyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblCompletedSurvey._meta.fields]


class TblAnswerQuestionsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblAnswerQuestions._meta.fields]


class TblQuestionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblQuestion._meta.fields]


class TblAnswerOptionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblAnswerOption._meta.fields]


admin.site.register(TblQuestion, TblQuestionAdmin)
admin.site.register(TblAnswerOption, TblAnswerOptionAdmin)
admin.site.register(TblSurvey, SurveyAdmin)
admin.site.register(TblParticipant, TblParticipantAdmin)
admin.site.register(TblCompletedSurvey, TblCompletedSurveyAdmin)
admin.site.register(TblAnswerQuestions, TblAnswerQuestionsAdmin)