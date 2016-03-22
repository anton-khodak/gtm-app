from modeltranslation.translator import translator, TranslationOptions
from history.models import PollHistory, News


class HistoryTranslationOptions(TranslationOptions):
    fields = ('name', 'text')


class NewsTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(PollHistory, HistoryTranslationOptions)
translator.register(News, NewsTranslationOptions)
