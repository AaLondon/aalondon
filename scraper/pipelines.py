# -*- coding: utf-8 -*-
from meetings.models import Meeting

class MeetingPipeline(object):
      def process_item(self, item, spider):
          print('yeboyes')
          meeting, created = Meeting.objects.update_or_create(code=item['code'],defaults=item)
          return meeting