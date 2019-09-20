from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class TicketTypeForm(forms.ModelForm):

    class Meta:
        model = TicketType
        exclude = ()


TicketTypeFormSet = inlineformset_factory(
    Event, TicketType, form=TicketTypeForm,
    fields=['name', 'amount'], extra=1, can_delete=True
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        exclude = ['author', 'slug']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('flyer'),
                Field('description'),
                Field('category'),
                Field('start_date'),
                Field('end_date'),
                Fieldset('Add tickets',
                    Formset('titles')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )
