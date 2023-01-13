from django import forms
from agents.models import Agent
from .models import Lead, Category


class LeadModelForm(forms.ModelForm):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none(), required=False)
    
    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "age",
            "agent"
        )
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(
            organisation=request.user.userprofile
        )
        super().__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    
    def __init__(self, *args, **kwargs):
        # agent choices need to dynamic
        request = kwargs.pop("request")
        agents = Agent.objects.filter(
            organisation=request.user.userprofile
        )
        super().__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class CategoryUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Lead.objects.none())
    
    class Meta:
        model = Lead
        fields = (
            "category",
        )
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        if user.is_organisor:
            org = user.userprofile
        else:
            org = user.agent.organisation
        categorys = Category.objects.filter(
            organisation=org
        )
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = categorys
