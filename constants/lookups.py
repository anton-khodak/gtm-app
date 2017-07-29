from ajax_select import register, LookupChannel

from constants.models import Speciality, City, Position, Hospital, Area


@register('speciality')
class SpecialityLookup(LookupChannel):

    model = Speciality
    min_length = 0
    plugin_options = {'minLength': 0}

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('area')
class AreaLookup(LookupChannel):

    model = Area
    min_length = 0
    plugin_options = {'minLength': 0}


    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('city')
class CityLookup(LookupChannel):

    model = City
    min_length = 0
    plugin_options = {'minLength': 0}

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('position')
class PositionLookup(LookupChannel):

    model = Position
    min_length = 0
    plugin_options = {'minLength': 0}

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('work')
class WorkLookup(LookupChannel):

    model = Hospital
    min_length = 0
    plugin_options = {'minLength': 0}

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
