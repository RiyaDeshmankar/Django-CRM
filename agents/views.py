from django.shortcuts import render, reverse
from django.views import generic
from leads.models import Agent
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from leads.models import UserProfile

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = forms.AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        agent = form.save(commit=False)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        agent.organisation = profile
        agent.save()
        return super().form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentUpdateView(LoginRequiredMixin, generic.UpdateView): 
    model = Agent 
    template_name = "agents/agent_update.html" 
    form_class=forms.AgentModelForm
    context_object_name = "agent" 
    
    def get_success_url(self): 
        return reverse("agents:agent-list") 
    def get_queryset(self): 
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    
class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    
    def get_success_url(self): 
        return reverse("agents:agent-list") 
    
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

