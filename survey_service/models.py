from django.db import models
from uuid import uuid4


class TblParticipant(models.Model):
    """Участник опроса"""
    full_name = models.CharField('полное имя', max_length=100)

    class Meta:
        verbose_name = 'участник опроса'
        verbose_name_plural = 'участники опроса'
        ordering = ['id']

    def __str__(self):
        return f'Участник №{self.id}'


class TblSurvey(models.Model):
    """Опрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    survey_name = models.CharField(max_length=20, null=True)
    survey_description = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    finish_time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'
        # ordering = ['-start_time']

    def __str__(self):
        return self.survey_name


class TblQuestion(models.Model):
    """Вопрос из опроса"""
    QUESTION_TYPE = (
        ("1", "ответ текстом"),
        ("2", "ответ с выбором одного варианта"),
        ("3", "ответ с выбором нескольких вариантов"),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    question_text = models.TextField()
    is_active = models.BooleanField(default=True)
    survey = models.ForeignKey(TblSurvey, on_delete=models.CASCADE, null=True)
    question_type = models.CharField(max_length=50, null=True, blank=True, choices=QUESTION_TYPE)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question_text


class TblAnswerOption(models.Model):
    """Вариант ответа на вопрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    text = models.CharField('вариант ответа', max_length=255)
    question = models.ForeignKey(
        TblQuestion,
        verbose_name='вопрос',
        related_name='answer_options',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'вариант ответа на вопрос'
        verbose_name_plural = 'варианты ответов на вопросы'

    def __str__(self):
        return self.text


class TblCompletedSurvey(models.Model):
    """Пройденный опрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    survey = models.ForeignKey(
        TblSurvey,
        verbose_name='опрос',
        related_name='results',
        on_delete=models.CASCADE,
    )
    participant = models.ForeignKey(
        TblParticipant,
        verbose_name='участник',
        related_name='results',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'пройденный опрос'
        verbose_name_plural = 'пройденные опросы'
        ordering = ['-survey']

    def __str__(self):
        return f'{self.survey.survey_name} - {self.participant}'


class TblAnswerQuestions(models.Model):
    """Ответы на вопросы"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    question = models.ForeignKey(
        TblQuestion,
        verbose_name='Вопрос',
        related_name='answer_to_question',
        on_delete=models.CASCADE,
    )
    answers = models.ManyToManyField(TblAnswerOption)
    completed_survey = models.ForeignKey(
        TblCompletedSurvey,
        verbose_name='пройденный опрос',
        related_name='answer_to_question',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'ответ на вопрос'
        verbose_name_plural = 'ответы на вопрос'
        ordering = ['-question']

    def __str__(self):
        return f'{self.question.question_text} - {self.answers}'