#!/usr/bin/python

from random import randint
import subprocess
from time import sleep

"""
A simple game script that just generates two characters and they fight each other. 
Initially based on AD&D 2nd edition mechanics but modified in a variety of ways. 
"""

class CHAR_CLASS():
    def __init__(self,level,name,class_name):
        self.level = level
        self.name = name
        self.stgth = dice(6) + dice (6) + dice (6)
        self.stgth =  dice(6) + dice (6) + dice (6) 
        self.dex =  dice(6) + dice (6) + dice (6)
        self.con =  dice(6) + dice (6) + dice (6)
        self.inte =  dice(6) + dice (6) + dice (6)
        self.wis =  dice(6) + dice (6) + dice (6)
        self.char =  dice(6) + dice (6) + dice (6)
        self.mana = 0
        if class_name.lower() == "warrior":
            self.warrior()
        elif class_name.lower() == "rouge":
            self.rouge()
        elif class_name.lower() == "mage":
            self.mage()
        elif class_name.lower() == "priest":
            self.priest()

       
    def warrior(self):
        self.hp = 0
        for i in range(1,(self.level+1)):
            self.hp += dice(10) + (self.con *.2)
        self.armor = 5
        self.dodge = round(.1 * self.dex)
        self.thac0 = 20 - self.level - (.2 * self.dex)
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

    def rouge(self):
        self.hp = 0
        for i in range(1,(self.level+1)):
            self.hp += dice(6) + (self.con *.2)
        self.armor = 10
        self.dodge = round(.4 * self.dex)
        self.thac0 = 20 - self.level - (.4 * self.dex)
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

    def mage(self):
        self.hp = 0
        for i in range(1,(self.level+1)):
            self.hp += dice(4) + (self.con *.2)
        self.armor = 10
        self.dodge = round(.1 * self.dex)
        self.thac0 = 20 - self.level - (.1 * self.dex)
        self.rangedmg = 0
        self.dmg = 4
        self.dmg_mod = self.stgth * .1
        self.mana = (10 + round( self.inte * .5)) * level
        self.initive = 0
        self.initive_mod = 2
        self.special_dmg_mod = 1 + (self.stgth * .1 )
        self.special_atk_mod = 1 + ( self.dex * .1)
        self.special_counter_mod = 4
        self.special_counter = 0
        self.crit_chance  = .1 * self.dex
        self.crit = self.dex/100

    def  priest(self):
        self.hp = 0
        for i in range(1,(self.level+1)):
            self.hp += dice(6) + (self.con *.2)
        self.armor = 10
        self.dodge = round(.1 * self.dex)
        self.thac0 = 20 - self.level - (.1 * self.dex)
        self.rangedmg = 0
        self.dmg = 6
        self.dmg_mod = self.stgth * .1
        self.mana = (10 + round( self.inte * .25)) * level
        self.initive = 0
        self.initive_mod = 2
        self.special_dmg_mod = 2 + (self.stgth * .3 )
        self.special_atk_mod = 2 + ( self.dex * .3)
        self.special_counter_mod = 4
        self.special_counter = 0
        self.crit_chance  = .1 * self.dex
        self.crit = self.dex/100


    def melee_damage(self):
       dmg =  int(round(dice(self.dmg))) + int(round(self.dmg_mod))
       if dice(100) <= round(self.crit_chance):
           dmg = dmg + (self.crit * dmg)
       return dmg

class MAGIC():
     def cure(self,caster,target):
         magic_class = "holy"
         magic_type = "white"
         effect = dice(8) * caster.level()
         target.hp += effect

     def protect(self,caster,target):
         magic_class = "holy"
         magic_type = "white"
         effect = 2 * caster.level()
         target.armor -= effect

     def XXXX(self,caster,target):
         magic_class = ""
         magic_type = ""
         effect = "" 
         target.YYY = "??"

def clear():
    subprocess.call("clear")    


def dice(mod):
    return randint(1,int(mod))

def print_stats(p1,p2):
    clear()
    print "%s                    %s" % (p1.name, p2.name)
    print "level:%i              level:%i" % (p1.level, p2.level)
    print "hp:%i                 hp:%i" % (p1.hp, p2.hp)
    print "mp:%i                 mp:%i" % (p1.mana, p2.mana)
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
    dmg = first.melee_damage()
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

   if p1.hp > 0 and p2.hp > 0:
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



Good = CHAR_CLASS(10,"Good","warrior")
Bad = CHAR_CLASS(10,"Bad","rouge")

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

