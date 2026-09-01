from django import forms

from .models import BusinessRequest


class BusinessRequestCreateForm(forms.ModelForm):
    class Meta:
        model = BusinessRequest
        fields = ("title", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}


class BusinessRequestWorkflowForm(forms.ModelForm):
    class Meta:
        model = BusinessRequest
        fields = ("category", "action_plan", "status")
        widgets = {"action_plan": forms.Textarea(attrs={"rows": 8})}
