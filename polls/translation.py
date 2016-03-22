from modeltranslation.translator import translator, TranslationOptions
from polls.models import Poll, Question, Answer


class PollTranslationOptions(TranslationOptions):
    fields = ('name',)

class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'question_text')

class AnswerTranslationOptions(TranslationOptions):
    fields = ('answer_text',)



translator.register(Poll, PollTranslationOptions)
translator.register(Question, QuestionTranslationOptions)
translator.register(Answer, AnswerTranslationOptions)