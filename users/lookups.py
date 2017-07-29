from ajax_select import register, LookupChannel

from users.models import UserProfile


@register('separate_users')
class SeparateUsersLookup(LookupChannel):

    model = UserProfile

    def get_query(self, q, request):
        return self.model.objects.filter(user__username__icontains=q).order_by('user__username')

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.user.username
