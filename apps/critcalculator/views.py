# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import math

# Create your views here.

def index(request):
    context = {
        'classes': Class.objects.all(),
        'bosses': Boss.objects.all(),
    }    
    return render(request, "critcalculator/index.html", context)

def calculate_process(request):
    if request.method == "POST":
        boss = Boss.objects.get(id=request.POST['boss'])        
        user_class = Class.objects.get(id=request.POST['class'])
        if 'skill' not in request.POST:
            skill = Skill.objects.get(id=70)
        else:
            skill = Skill.objects.get(id=request.POST['skill'])

        if 'aura' not in request.POST:
            aura = 0
        else:
            aura = request.POST['aura']    
        if 'food' not in request.POST:
            food = 0
        else:
            food = request.POST['food']  

        if 'w_stance' in request.POST:
            print "w_stance = ", request.POST['w_stance']
            if request.POST['w_stance'] == "1":
                Cf = 55
                G = 0
            else:
                Cf = 0
                G = 0.15
        else:
            Cf = 0
            G = 0
        A = float(request.POST['race']) + float(request.POST['crystal']) + skill.a
        B = skill.b
        D = float(request.POST['direction'])
        G = G + skill.g
        I = skill.i
        L = boss.level_diff
        T = boss.mobtype
        CR = boss.cr
        Cfo = user_class.base_cf
        Cf = Cf + float(request.POST['bonus_cf'])+ Cfo * float(aura) + float(food)        
        F = (3*L*T)/(400*I*(2*G + 1))
        total_crit = (B*Cfo + Cf)
        n = ((D*I*(B*Cfo + Cf)) / (10*CR)) + F
        if n > 1:
            CC = 1
        else:      
            CC = n + G*(A+n)*(1-n)

        # print "================ ", user_class.name  
        # print "aura = ", aura         
        # print "food = ", food   
        # print "A = ", A 
        # print "B = ", B
        # print "D = ", D
        # print "G = ", G        
        # print "I = ", I
        # print "boss name = ", boss.name        
        # print "L = ", L
        # print "T = ", T
        # print "CR = ", CR
        # print "Cfo = ", Cfo
        # print "Cf = ", Cf
        # print "total crit = ", total_crit
        # print "F = ", F
        # print "n = ", n  
        # print "CC = ", CC
                 
    return HttpResponse(math.floor((CC)*100))



def get_class_skill(request):
    if request.is_ajax() and request.method == "POST":
        skills = Skill.objects.filter(of_class__id=request.POST['class_id']).order_by("name")
        return render(request, "critcalculator/skill.html", { "skills": Skill.objects.filter(of_class__id=request.POST['class_id'])})
    return redirect('/')
def add(request):
    return render(request, "critcalculator/add_skill.html")


def add_skill_process(request):
    if request.method == "POST":
        print request.POST
        user_class = Class.objects.get(id=request.POST['class'])
        print user_class.name
        Skill.objects.create(name=request.POST['name'], g=request.POST['g'], i=request.POST['i'], b=request.POST['b'], a=request.POST['a'], of_class=user_class)
    return redirect('/add')

