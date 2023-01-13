from django.views import  generic
from django.shortcuts import reverse, redirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Category
from .forms import LeadModelForm, AssignAgentForm, CategoryUpdateForm


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse("leads:lead-list"))
        return super().get(*args, **kwargs)


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    
    def get_queryset(self):
        # only agent assigned leads
        user = self.request.user
        queryset = Lead.objects.all()
        if user.is_organisor: # if organisor
            queryset = queryset.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else: # if agent
            queryset = queryset.filter(
                agent=user.agent,
                agent__isnull=False
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        # add unassigned_leads to context
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
        if user.is_organisor: # if organisor
            queryset = queryset.filter(organisation=user.userprofile)
        else: # if agent
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        """
        before saving leads set lead organisation, category(recent)
        and send email
        """
        lead = form.save(commit=False)
        org = self.request.user.userprofile # organisation
        lead.organisation = org
        recent_category = Category.objects.filter(organisation=org).filter(name="Recent").get()
        lead.category = recent_category
        lead.save()
        # send mail
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super().form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        return Lead.objects.filter(organisation=self.request.user.userprofile)


class AssignAgentView(OrganisorAndLoginRequiredMixin,generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        if user.is_organisor: # if organisor
            queryset = queryset.filter(
                organisation=user.userprofile
            )
        else: # if agent
            queryset = queryset.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryUpdateForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
        if user.is_organisor:
            queryset = queryset.filter(organisation=user.userprofile)
        else:
            queryset = queryset.filter(organisation=user.agent.organisation)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:category-list")
