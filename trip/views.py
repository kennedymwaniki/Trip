from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView
# Create your views here.
from .models import Trip, Note


class HomeView(TemplateView):
    template_name = 'trip/index.html'


def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        'trips': trips
    }
    return render(request, 'trip/trip_list.html', context)


class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # expected template is the model name(model_form.html)
    # the form instance is passed in from the view
    # this will get triggered whenever the form is submitted

    def form_valid(self, form):
        # owner == logged in user
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TripDetailView(DetailView):
    model = Trip
    # show notes related to a trip by overriding

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context["object"]
        notes = trip.notes.all()
        context['notes'] = notes
        return context


class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ["city", "country", "start_date", "end_date"]
    # template named model_form.html


class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')


# Notes

class NoteListView(ListView):
    model = Note

    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user)
        return queryset


class NoteDetailView(DetailView):
    model = Note
    fields = ['name', 'description', 'type']


class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = "__all__"

    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form


class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = "__all__"

    def get_form(self):
        form = super(NoteUpdateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')
    # not make the template - send post requests here
