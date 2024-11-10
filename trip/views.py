from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from .models import Trip, Note


class HomeView(TemplateView):
    template_name = 'trip/index.html'


def trips_list(request):
    trips = Trip.objects.all()
    context = {
        'trips': trips
    }
    return render(request, 'trip/trip_list.html', context)
