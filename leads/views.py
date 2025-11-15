from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse 
from . import models
from agents.mixins import OrganisorAndLoginRequiredMixin
from . import forms 
from . models import Lead
from django.views import generic

#class based view
class SignupView(generic.CreateView):
    template_name='registration/signup.html'
    form_class=forms.CustomUserCreationForm
     
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    
    
class LandingPagebView(generic.TemplateView):  #we use generic to increase usability & not to write unecessary things
    template_name="landing.html"

#fxn based views
def landing_page(req):
    return render(req,'landing.html')

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            # Show only assigned leads for the organiser in main list
            queryset = models.Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            # Agent sees only leads assigned to them
            queryset = models.Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__user=user
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            # Show only leads where agent is NULL
            unassigned_leads = models.Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context["unassigned_leads"] = unassigned_leads

        return context


def lead_list(req): #Display a list of all leads
    leads= models.Lead.objects.all()
    context={
        'leads':leads
    }
    return render(req, 'leads/lead_list.html', context)  


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name="leads/lead_detail.html"
    context_object_name="lead"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=models.Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=models.Lead.objects.filter(organisation=user.agent.organisation)
        
            queryset=queryset.filter(agent__user=user)
        return queryset


def lead_detail(req, pk ): #retrieves lead details using primary key
    lead= models.Lead.objects.get(id=pk)
    context={
        'lead': lead
    }
    return render(req,"leads/lead_detail.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = forms.LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()

        # Send notification (optional)
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead.",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )

        return super().form_valid(form)


def lead_create(req): #creates new lead
    form= forms.LeadModelForm()
    if req.method=="POST":
        form=forms.LeadModelForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads/all")
    context={
        'form': form #we can use the word forms anywhere inside the file
    }
    return render(req,'leads/lead_create.html',context)



class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name="leads/lead_update.html"
    form_class= forms.LeadModelForm
    def get_queryset(self):
        user=self.request.user
        return models.Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(req,pk):
    lead= models.Lead.objects.get(id=pk)
    form= forms.LeadModelForm(instance=lead)
    if req.method=="POST":
        form=forms.LeadModelForm(req.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads/all")
    context={
        'form':form,
        'lead': lead #we can use the word forms anywhere inside the file
    }
    return render(req,'leads/lead_update.html',context)



class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name="leads/lead_delete.html"
    def get_queryset(self):
        user=self.request.user
        return models.Lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(req,pk):
    lead= models.Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads/all")
    

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name='leads/assign_agent.html'
    form_class=forms.AssignAgentForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs=super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent=form.cleaned_data["agent"]
        lead= Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
            unassigned_lead_count = models.Lead.objects.filter(
                organisation=user.userprofile,
                category__isnull=True
            ).count()
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation,
            )
            unassigned_lead_count = models.Lead.objects.filter(
                organisation=user.agent.organisation,
                category__isnull=True
            ).count()
        
        context.update({
            "unassigned_lead_count": unassigned_lead_count
        })
        return context
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation,
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name="leads/category_detail.html"
    context_object_name="category" 
    
    def get_queryset(self):
            user = self.request.user
            if user.is_organisor:
                queryset = models.Category.objects.filter(
                    organisation=user.userprofile
                )
            else:
                queryset = models.Category.objects.filter(
                    organisation=user.agent.organisation,
                )
            return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name="leads/lead_category_update.html"
    form_class=forms.LeadCategoryUpdateForm
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=models.Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=models.Lead.objects.filter(organisation=user.agent.organisation)
        
            queryset=queryset.filter(agent__user=user)
        return queryset
    def get_success_url(self):
        return reverse("leads:lead-details", kwargs={'pk':self.get_object().id})
