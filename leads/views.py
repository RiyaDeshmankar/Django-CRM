from django.shortcuts import render, redirect
from . import models
from . import forms
#fxn based views
def lead_list(req): #Display a list of all leads
    leads= models.Lead.objects.all()
    context={
        'leads':leads
    }
    return render(req, 'leads/lead_list.html', context)  

def lead_detail(req, pk ): #retrieves lead details using primary key
    lead= models.Lead.objects.get(id=pk)
    context={
        'lead': lead
    }
    return render(req,"leads/lead_detail.html", context)


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
