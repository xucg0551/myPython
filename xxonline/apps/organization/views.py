from django.shortcuts import render, HttpResponse
from django.views.generic import View

# Create your views here.

class OrgView(View):
    def get(self, request):
        # return HttpResponse('fsadfafafsafa', content_type='text/plain')
        return render(request, 'org-list.html')

