from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
# class account(models.Model):
# username = models.CharField(max_length=20, null=False)
# password = models.CharField(max_length=20, null=False)
# fullname = models.CharField(max_length=50)
# dob = models.DateField('Date of Birth')
# gender = models.BooleanField('Gender')
# address = models.CharField(max_length=100)
# email = models.EmailField(max_length=30)
# phone = models.CharField(max_length=15)


class leagues(models.Model):

    class TeamsChoice(models.IntegerChoices):
        EIGHT = 8
        SIXTEEN = 16
        THIRTY_TWO = 32

    class AgeChoice(models.IntegerChoices):
        TWELVE = 12, _('U12')
        SIXTEEN = 16, _('U16')
        NINETEEN = 19, _('U19')
        TWENTY_THREE = 23, _('U23')

    class StadiumChoice(models.IntegerChoices):
        FIVE = 5,
        ELEVEN = 11

    class StateChoice(models.TextChoices):
        NOT_STARTED = 'NS', _('Not started')
        IN_PREPARATION = 'PR', _('In preparation')
        IN_PROGRESS = 'ON', _('In progress')
        ENDED = 'OFF', _('Ended')

    name = models.CharField(max_length=50, null=False)
    numOfTeams = models.IntegerField(
        'Number of teams', choices=TeamsChoice.choices, null=False)
    format = models.CharField('Format', max_length=30, default='Round robin')
    ageLimit = models.IntegerField(
        'Age', choices=AgeChoice.choices, null=False)
    entryFee = models.IntegerField(default=0)
    stadiumType = models.IntegerField(choices=StadiumChoice.choices)
    displayMode = models.BinaryField('Visibility', default=0)
    state = models.TextField(choices=StateChoice.choices,
                             default=StateChoice.NOT_STARTED)


class match(models.Model):
    matchNum = models.PositiveSmallIntegerField('Match number')
    time = models.DateTimeField('Kick-off time')
    stadium = models.CharField('Stadium')
    # referee = models.


class referee(models.Model):
    name = models.CharField(max_length=50, null=False)


class match_info(models.Model):
    goalA = models.PositiveSmallIntegerField('Num of A goals', default=0)
    goalB = models.PositiveSmallIntegerField('Num of B goals', default=0)
    cardA = models.PositiveSmallIntegerField('Num of A card', default=0)
    cardB = models.PositiveSmallIntegerField('Num of B cards', default=0)


class goals(models.Model):
    goalCode = models.PositiveSmallIntegerField('Goal No.')
    time = models.PositiveSmallIntegerField('Time')


class lineup(models.Model):
    class StatusChoices(models.TextChoices):
        STARTING = 'L11', _('Starting 11')
        SUBSTITUTE = 'S', _('Substitution')
        NOT_PARTICIPATED = 'DNP', _('Reserved')

    status = models.TextField(choices=StatusChoices.choices)


class standing(models.Model):
    pass


class team(models.Model):
    pass


class coaches(models.Model):
    pass


class players(models.Model):
    pass


class assistants(models.Model):
    pass
