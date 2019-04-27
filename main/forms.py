from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import StudentList, Scaffold


class StudentListForm(forms.ModelForm):
    class Meta:
        model = StudentList
        fields = ('year_choices', 'cohort_choices', 'sl_xls', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload Student list'))


class ScaffoldForm(forms.ModelForm):
    class Meta:
        model = Scaffold
        fields = ('year_choices', 'cohort_choices', 'module', 'pdf', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload Scaffold'))