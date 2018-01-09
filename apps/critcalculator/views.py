# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division



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
        if 'class' not in request.POST:
            user_class = Class.objects.first()           
        else:
            user_class = Class.objects.get(id=request.POST['class'])
        if 'boss' not in request.POST:
            boss = Boss.objects.first()    
        else:
            boss = Boss.objects.get(id=request.POST['boss'])        
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
            # print "w_stance = ", request.POST['w_stance']
            if request.POST['w_stance'] == "1":
                Cf = 55
                G = 0
            else:
                Cf = 0
                G = 0.15
        else:
            Cf = 0
            G = 0
        if 'crackshot' in request.POST:
            # print "crack shot is on"
            A = 0.1
        else:
            A = 0
        A = A + float(request.POST['race']) + float(request.POST['crystal']) + skill.a
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

        print "================ ", user_class.name  
        print "aura = ", aura         
        print "food = ", food   
        print "A = ", A 
        print "B = ", B
        print "D = ", D
        print "G = ", G        
        print "I = ", I
        print "boss name = ", boss.name        
        print "L = ", L
        print "T = ", T
        print "CR = ", CR
        print "Cfo = ", Cfo
        print "Cf = ", Cf
        print "total crit = ", total_crit
        print "F = ", F
        print "n = ", n  
        print "CC = ", CC
                 
    return HttpResponse(math.floor((CC)*100))



def get_class_skill(request):
    if request.is_ajax() and request.method == "POST":
        skills = Skill.objects.filter(of_class__id=request.POST['class_id']).order_by("name")
        context = {
            "class": request.POST['class_id'],
            "skills": Skill.objects.filter(of_class__id=request.POST['class_id']),
            'mystic_crit': Class.objects.get(id=request.POST['class_id']).base_cf * 1.2
        }        
        return render(request, "critcalculator/skill.html", context)
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

def calculate_damage_process(request):
    if request.method == "POST":
        print request.POST
        multiplier = 2+1.42
        if 'focus' in request.POST:
            multiplier += float(request.POST['focus'])
        if 'savage' in request.POST:
            multiplier += float(request.POST['savage'])  
        if 'bitter' in request.POST:
            multiplier += float(request.POST['bitter'])   
        if 'slaying' in request.POST:
            multiplier += float(request.POST['slaying'])   
        if 'wrathful' in request.POST:
            multiplier += float(request.POST['wrathful'])  
        current_power = float(request.POST['current_power'])
        current_crit = float(request.POST['current_crit'])
        next_power = float(request.POST['next_power'])
        next_crit = float(request.POST['next_crit'])
        print multiplier
        number_of_hit = 1000
        current_damage_per_hit = 1000        
        next_damage_percentage = ((next_power+100) / (current_power+100))
       
        next_damage_per_hit = current_damage_per_hit * next_damage_percentage
        print "next_damage_per_hit = ", next_damage_per_hit
        current_damage = (number_of_hit * current_crit * current_damage_per_hit * multiplier) + (number_of_hit * (1-current_crit) * current_damage_per_hit)
        print "current_damage = ", current_damage
        next_damage = (number_of_hit * next_crit * next_damage_per_hit * multiplier) + (number_of_hit * (1-next_crit) * next_damage_per_hit)
        print "next_damage = ", next_damage 
        percent_change = ((next_damage - current_damage) / current_damage) * 100
    return HttpResponse(round(percent_change,2))