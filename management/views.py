"""
Views for order management.
"""
from datetime import datetime, timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from tozd.settings import PRICE_ZABOJ
from users.models import Distributer
from zaboj.models import Order, Crate
from .models import ZabojProduction, ZabojDistribution

class OrdersList(PermissionRequiredMixin, ListView):
    """
    View all orders and filter them.
    """
    permission_required = 'is_staff'
    model = Order
    template_name = 'management/orders.html'
    end = datetime.now()
    past_week = datetime.now() - timedelta(days=14)

    def get_queryset(self):
        filter_val = self.request.GET.get('show_processed', None)
        if filter_val:
            queryset = Order.objects.all().order_by('-created')
        else:
            queryset = Order.objects.exclude(id__in=ZabojProduction.objects.values_list('order')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """ Additional context. """
        context = super(OrdersList, self).get_context_data(**kwargs)
        context['show_processed'] = self.request.GET.get('show_processed', False)
        return context

class ProcessOrder(CreateView):
    """
    Fill out production details
    """
    model = ZabojProduction
    template_name = 'management/fillout_order.html'
    fields = ['crate', 'distribution_notes', 'enduser_notes', 'assign_to', 'price']

    def get_initial(self):
        order = get_object_or_404(Order, id=self.kwargs.get('order'))
        distributer = Distributer.objects.filter(district=order.user.district).first()
        return {
            'assign_to': distributer,
            'price':order.quantity*PRICE_ZABOJ
        }

    def form_valid(self, form):
        # move crate to the distributer
        crate = get_object_or_404(Crate, id=form.instance.crate.id)
        crate.at_distributer = form.instance.assign_to
        crate.save()
        form.instance.order = get_object_or_404(Order, id=self.kwargs.get('order'))
        form.instance.prepared_by = self.request.user
        return super(ProcessOrder, self).form_valid(form)

class DeliveriesDistributerList(PermissionRequiredMixin, ListView):
    """
    View all orders and filter them.
    """
    permission_required = 'is_staff'
    model = ZabojProduction
    template_name = 'management/deliveries.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('show_delivered', None)
        user = get_object_or_404(Distributer, user=self.request.user)
        if filter_val:
            queryset = ZabojProduction.objects.filter(assign_to=user).order_by('-created')
        else:
            queryset = ZabojProduction.objects.filter(assign_to=user).exclude(id__in=ZabojDistribution.objects.values_list('package')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """ Additional context. """
        context = super(DeliveriesDistributerList, self).get_context_data(**kwargs)
        context['show_delivered'] = self.request.GET.get('show_delivered', False)
        return context

class DeliveriesAllList(PermissionRequiredMixin, ListView):
    """
    View all orders and filter them.
    """
    permission_required = 'is_staff'
    model = ZabojProduction
    template_name = 'management/deliveries.html'

    def get_queryset(self):       
        filter_val = self.request.GET.get('show_delivered', None)
        if(filter_val):
            queryset = ZabojProduction.objects.all().order_by('-created')
        else:
            queryset = ZabojProduction.objects.exclude(id__in=ZabojDistribution.objects.values_list('package')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Additional context.
        """
        context = super(DeliveriesAllList, self).get_context_data(**kwargs)
        context['show_delivered'] = self.request.GET.get('show_delivered', False)
        return context

class DeliverOrder(CreateView):
    """
    Edit the delivery status.
    """
    model = ZabojDistribution
    template_name = 'management/fillout_delivery.html'
    fields = ['money_received', 'is_extra_donation', 'notes']

    def get_initial(self):
        package = get_object_or_404(ZabojProduction, id=self.kwargs.get('package'))
        return {
            'money_received': package.price,
        }

    def form_valid(self, form):
        package = get_object_or_404(ZabojProduction, id=self.kwargs.get('package'))
        # move crate to the end user
        crate = package.crate
        order = package.order
        crate.at_distributer = None
        crate.at_user = order.user
        crate.save()
        form.instance.package = package
        form.instance.delivered_by = self.request.user
        return super(DeliverOrder, self).form_valid(form)