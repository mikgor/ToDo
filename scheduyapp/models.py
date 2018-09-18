from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import pytz
from django.utils.translation import ugettext_lazy as _

class TaskGroup(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=30, default="whitesmoke")

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(_('Name'), max_length=40)
    details = models.CharField(_('Details'), max_length=80, blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(_('Deadline'))
    priority = models.PositiveSmallIntegerField(_('Priority'), default=1)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, verbose_name = _('Group'))

    def __str__(self):
        return self.name

    def isExpired(self):
        now = datetime.now(timezone.utc)
        return now > self.deadline

    def remainingTime(self):
        secondsTotal = 0
        days = 0
        hours = 0
        mins = 0
        now = datetime.now(pytz.timezone('UTC'))
        secondsTotal = (self.deadline - now).total_seconds()
        if secondsTotal < 0: # when isExpired
            secondsTotal = secondsTotal * -1
        if secondsTotal >= 24*3600: # 1 day
            secondsOffset = secondsTotal % (24*3600)
            days = int((secondsTotal - secondsOffset) / (24*3600))
            secondsTotal = secondsOffset
        if secondsTotal >= 3600: # 1 hour
            secondsOffset = secondsTotal % 3600
            hours = int((secondsTotal - secondsOffset) / 3600)
            secondsTotal = secondsOffset
        if secondsTotal >= 60:
            secondsOffset = secondsTotal % 60
            mins = int((secondsTotal - secondsOffset) / 60)
        text = 'ago' if self.isExpired() else 'remaining'
        if days < 1 and hours < 1:
            return '{} m {}'.format(mins, text)
        elif days < 1:
            return '{} h, {} m {}'.format(hours, mins, text)
        else:
            return '{} d, {} h, {} m {}'.format(days, hours, mins, text)

    def remainingTimeSeconds(self):
        now = datetime.now(pytz.timezone('UTC'))
        return (self.deadline - now).total_seconds()

    def setIsDone(self):
        if self.is_done:
            self.is_done = False
        else:
            self.is_done = True
        self.save()

class AppUser(AbstractUser):
    taskGroups = models.ManyToManyField(TaskGroup)
    tasks = models.ManyToManyField(Task)
    showDonePreference = models.BooleanField(default=False)
    timezonePreference = models.CharField(_('Timezone'), max_length=32, choices=tuple(zip(pytz.all_timezones, pytz.all_timezones)), default='UTC')
    languagePreference = models.CharField(_('Language'), max_length=32, choices=settings.LANGUAGES, default='en')
    taskOrderPreference = models.CharField(_('Task order'), max_length=20, default='-priority')

    def __str__(self):
        return self.email

    def GetTasks(self):
        if self.showDonePreference == False:
            return self.tasks.filter(is_done=False).order_by(self.taskOrderPreference)
        return self.tasks.all().order_by(self.taskOrderPreference)

    def GetTaskGroups(self):
        return self.taskGroups.filter(id__in=self.GetTasks().values("group"))

    def SetShowDonePreference(self):
        if self.showDonePreference:
            self.showDonePreference = False
        else:
            self.showDonePreference = True
        self.save()

    def SetTimezonePreference(self, timezone):
        if "etc/gmt" in timezone.lower():
            timezone = timezone.replace(" ", "+")
        if timezone in pytz.all_timezones:
            self.timezonePreference = timezone
            self.save()

    def SetLanguagePreference(self, language):
        for l in settings.LANGUAGES:
            if language in l:
                self.languagePreference = language
                self.save()

    def SetTaskOrderPreference(self, order):
        self.taskOrderPreference = order
        self.save()
