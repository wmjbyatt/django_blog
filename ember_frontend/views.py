from django.views import generic
from django.conf import settings

class MainView(generic.TemplateView):
  template_name = 'index.htm'

main_page = MainView.as_view()
