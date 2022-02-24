from ajax_select import register, LookupChannel
from .models import *

@register('author-lookup')
class AuthorLookup(LookupChannel):

    model = Author

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

    def check_auth(self, request):
        pass

@register('aff-lookup')
class AffLookup(LookupChannel):

    model = Affiliation 

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

    def check_auth(self, request):
        pass