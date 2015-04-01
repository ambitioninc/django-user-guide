from django.http import HttpResponse
from django.views.generic import View

from user_guide import models


class GuideSeenView(View):
    def post(self, request):
        guide_id = request.POST.get('id', 0)
        is_finished = request.POST.get('is_finished', False)
        guide_info = models.GuideInfo.objects.get(id=guide_id)

        if guide_info and guide_info.user.id == request.user.id and is_finished:
            guide_info.is_finished = True
            guide_info.save()

        return HttpResponse(status=200)
