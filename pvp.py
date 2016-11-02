#!/usr/bin/python
"""
A simple game script that just generates two characters and they fight each other. 
Initially based on AD&D 2nd edition mechanics but modified in a variety of ways. 

"""

from random import randint
import subprocess
from time import sleep



class WARRIOR():
    def __init__(self,level,name):
        self.level = level
        self.name = name
        self.stgth = dice(20)
        if self.stgth < 10:
            while self.stgth < 10:
                self.stgth = dice(20)
        self.dex = dice(20)
        self.con = dice(20)
        if self.con < 10:
            while self.con < 10:
                self.con = dice(20)
        self.inte = dice(20)
        self.wis = dice(20)
        self.char = dice(20) 
        self.hp = 0
        for i in range(1,(level+1)):
            self.hp += dice(10) + (self.con *.2)
        self.armor = 5
        self.dodge = round(.1 * self.dex)
        self.thac0 = 20 - level - (.2 * self.dex) 
        self.rangedmg = 4
        self.dmg = 8
        self.dmg_mod = self.stgth * .2
        self.initive = 0
        self.initive_mod = 0
        self.special_dmg_mod = 2 + (self.stgth * .1 )
        self.special_atk_mod = 2 + ( self.dex * .1)
        self.special_counter_mod = 1
        self.special_counter = 0
        self.crit_chance  = .1 * self.dex
        self.crit = self.dex/100
    def damage(self):
       dmg =  int(round(dice(self.dmg))) + int(round(self.dmg_mod))
       if dice(100) <= round(self.crit_chance):
           dmg = dmg + (self.crit * dmg)
       return dmg
        

class ROUGE():
    def __init__(self,level,name):
        self.level = level
        self.name = name
        self.stgth = dice(20)
        self.dex = dice(20)
        if self.dex < 10:
            while self.dex < 10:
                self.dex = dice(20)
        self.con = dice(20)
        self.inte = dice(20)
        self.wis = dice(20)
        self.char = dice(20)
        self.hp = 0
        for i in range(1,(level+1)):
            self.hp += dice(6) + (self.con *.2)
        self.armor = 10
        self.dodge = round(.4 * self.dex)
        self.thac0 = 20 - level - (.4 * self.dex)
        self.rangedmg = 6
        self.dmg = 4
        self.dmg_mod = self.stgth * .2
        self.initive = 0
        self.initive_mod = 2
        self.special_dmg_mod = 4 + (self.stgth * .3 )
        self.special_atk_mod = 4 + ( self.dex * .3)
        self.special_counter_mod = 4
        self.special_counter = 0
        self.crit_chance  = .4 * self.dex
        self.crit = self.dex/100
    def damage(self):
       dmg =  int(round(dice(self.dmg))) + int(round(self.dmg_mod))
       if dice(100) <= round(self.crit_chance):
           dmg = dmg + (self.crit * dmg)
       return dmg



def clear():
    subprocess.call("clear")    


def dice(mod):
    return randint(1,int(mod))

def print_stats(p1,p2):
    clear()
    print "%s                    %s" % (p1.name, p2.name)
    print "level:%i              level:%i" % (p1.level, p2.level)
    print "hp:%i                 hp:%i" % (p1.hp, p2.hp)
    print "str:%i dex:%i con:%i || str:%i dex:%i con:%i" \
    % ( p1.stgth, p1.dex, p1.con, p2.stgth, p2.dex, p2.con)
    print "thac0:%i               thac0:%i" % (p1.thac0, p2.thac0)
    print "armor:%i               armor:%i:" % (p1.armor, p2.armor)
    print "dmg:%i                 dmg:%i" % (p1.dmg, p2.dmg) 
    print "special:%i             special:%i" % (p1.special_counter, p2.special_counter) 
    print "initive:%i             initive:%i" % (p1.initive, p2.initive)
    print "==========================================="

def dmg(first,second):
    atk = dice(20) - second.dodge
    dmg = first.damage()
    if first.special_counter >= 10:
        atk *= int(round(first.special_atk_mod))
        dmg *= int(round(first.special_dmg_mod))
        first.special_counter = 0
        print "INCOMING SPECIAL"
    if atk >= first.thac0-second.armor:
        print "Hit for " + str(dmg)
        second.hp -= int(dmg)
        first.special_counter += first.special_counter_mod 
    else:
        print "miss"
        first.special_counter += first.special_counter_mod - 1


def rollinit(p1,p2):
    p1.initive = dice(10) - p1.initive_mod
    p2.initive = dice(10) - p2.initive_mod
    while p1.initive == p2.initive:
        p1.initive = dice(10)
        p2.initive = dice(10)

def fight_round(p1,p2):
   token = ""
   if p1.initive < p2.initive:
      print p1.name + " goes first"
      dmg(p1,p2)
      token = p2.name
   elif p2.initive < p1.initive:
      print p2.name + " goes first"
      dmg(p2,p1)
      token = p1.name
   else:
       print "errors are occuring"

   print token + "is next"
   
   if token == p1.name:
       print p1.name + " turn"
       dmg(p1,p2)
       p1.special_counter += 1
   elif token == p2.name:
       print p2.name + " turn"
       dmg(p2,p1)
       p1.special_counter += 1
   else:
       print "errors are occuring"



Good = WARRIOR(10,"Good")
Bad = ROUGE(10,"Bad")

clear()
print_stats (Good,Bad)
counter =1

while Good.hp > 0 and Bad.hp > 0:
    rollinit(Good,Bad)
    print_stats(Good,Bad)
    print "fight round %i" % counter
    fight_round(Good,Bad)
    counter += 1
    sleep(3)


print_stats(Good,Bad)

