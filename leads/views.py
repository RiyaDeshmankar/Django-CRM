from django.shortcuts import render, redirect
from django.urls import reverse 
from . import models
from . import forms
from django.views import generic
#class based view
class LandingPagebView(generic.TemplateView):  #we use generic to increase usability & not to write unecessary things
    template_name="landing.html"

#fxn based views
def landing_page(req):
    return render(req,'landing.html')


class LeadListView(generic.ListView):
    template_name="leads/lead_list.html"
    queryset=forms.Lead.objects.all()
    context_object_name="leads"

def lead_list(req): #Display a list of all leads
    leads= models.Lead.objects.all()
    context={
        'leads':leads
    }
    return render(req, 'leads/lead_list.html', context)  


class LeadDetailView(generic.DetailView):
    template_name="leads/lead_detail.html"
    queryset=forms.Lead.objects.all()
    context_object_name="lead"

def lead_detail(req, pk ): #retrieves lead details using primary key
    lead= models.Lead.objects.get(id=pk)
    context={
        'lead': lead
    }
    return render(req,"leads/lead_detail.html", context)


class LeadCreateView(generic.CreateView):
    template_name="leads/lead_create.html"
    form_class= forms.LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")

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


class LeadUpdateView(generic.UpdateView):
    template_name="leads/lead_update.html"
    queryset=forms.Lead.objects.all()
    form_class= forms.LeadModelForm
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


class LeadDeleteView(generic.DeleteView):
    template_name="leads/lead_delete.html"
    queryset=forms.Lead.objects.all()
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(req,pk):
    lead= models.Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads/all")
    
# def lead_create(req): 
    # form= forms.LeadForm()
    # if req.method=="POST":
    #     form=forms.LeadForm(req.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         first_name=form.cleaned_data['first_name']
    #         last_name=form.cleaned_data['last_name']
    #         age=form.cleaned_data['age']
    #         agent= models.Agent.objects.first()
            
    #         models.Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         return redirect("/leads/all")
    # context={
#         'form': form #we can use the word forms anywhere inside the file
#     }
#     return render(req,'leads/lead_create.html',context)
