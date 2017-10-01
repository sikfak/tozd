"""
Models for management - production, distribution, stornation, etc.
"""
from django.db import models
from zaboj.models import Order, Crate
from users.models import Distributer
from tozd.settings import AUTH_USER_MODEL as User

class ZabojStorno(models.Model):
    """
    If there is a storno we should collect some data instead of just deleting the order.
    """
    order = models.ForeignKey(Order)
    reason = models.TextField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Strono for: {self.order}'

class ZabojProduction(models.Model):
    """
    When a crate is prepared this is entered
    """
    order = models.ForeignKey(Order)
    prepared_by = models.ForeignKey(User)
    crate = models.ForeignKey(Crate)
    assign_to = models.ForeignKey(Distributer)
    distribution_notes = models.TextField(max_length=140, blank=True, null=True)
    enduser_notes = models.TextField(max_length=140, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created.strftime('%#d. %#m. %Y')  + ' prepared by ' + str(self.prepared_by) \
    + ' for (' + str(self.order) + ')'

    def get_absolute_url(self):
        """
        Redirect after edit.
        """
        return '/mng/orders'

class ZabojDistribution(models.Model):
    """
    Model for distribution.
    """
    package = models.ForeignKey(ZabojProduction)
    delivered_by = models.ForeignKey(User)
    money_received = models.DecimalField(max_digits=5, decimal_places=2)
    is_extra_donation = models.BooleanField(default=False)
    notes = models.TextField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created.strftime('%#d. %#m. %Y')  + ' delivered by ' + str(self.delivered_by) \
    + ' for (' + str(self.package.order) + ')'

    def get_absolute_url(self):
        """ Redirect after edit. """
        return '/mng/distribution'
