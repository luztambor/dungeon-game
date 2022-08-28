import random
import tkinter as tk
import tkinter.messagebox as tkm


#Main function called
def main():
    game.currentroom=r31
    game.dialogue.tag_config('desc', foreground="blue")
    game.dialogue.tag_config('item', foreground="red")
    game.gameprint("Welcome to Room Explorer, young traveller. Use the navigation keys to travel.")
    game.currentroom=r31
    game.gameprint(game.currentroom.description,'desc')
    game.updateInfo()
    tk.mainloop()


class Game: #main GUI
    def __init__(self):
        #Create window, title it Room Explorer
        self.window = tk.Tk()
        self.window.title("Room Explorer")
        #Create 800x400 Canvas for GUI
        self.canvas=tk.Canvas(self.window,width=800,height=400)
        self.canvas.grid()


        #Create dialogue box, place in row 0 of whole window
        self.dialogue=tk.Text(self.window,width=110,height=30,relief='ridge',bd=3)
        self.dialogue.grid(row=0, sticky=tk.N,pady=1)
        #Disables dialogue box so that user can't type in it
        self.dialogue.configure(state="disabled")


        #Create frame for bottom, contains the rest of the widgets, row 1 of whole window
        self.bottomframe = tk.Frame(self.window)
        self.bottomframe.grid(row=1)


        #Create LabelFrame for movement, put into column 0 for bottomframe
        self.movement = tk.LabelFrame(self.bottomframe,text="Travel",relief='ridge',labelanchor='n')
        self.movement.grid(row=0, column=0, sticky=tk.W,padx=10)
        #Create Movement Buttons in LabelFrame
        self.button1 = tk.Button(self.movement, text="N", width=1)
        self.button1.grid(row=1, column=1)
        self.button1['command'] = self.moveUp


        self.button2 = tk.Button(self.movement, text="S", width=1)
        self.button2.grid(row=3, column=1)
        self.button2['command']=self.moveDown


        self.button3 = tk.Button(self.movement, text="W", width=1)
        self.button3.grid(row=2, column=0)
        self.button3['command']=self.moveLeft


        self.button4 = tk.Button(self.movement, text="E", width=1)
        self.button4.grid(row=2, column=2)
        self.button4['command']=self.moveRight


        #Create LabelFrame for map, put into column 1 for bottomframe
        self.map = tk.LabelFrame(self.bottomframe,text="Map",relief='ridge',labelanchor='n')
        self.map.grid(row=0, column=1, sticky=tk.W, padx=10)
        #Place an image of 5x5 grid into map frame
        #Below function decodes base64 encoded 5x5 grid .gif
        self.base='''R0lGODlhWgBaAPABAAAAAP///yH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sOZ2FtbWE9MC40NTQ1NDUALAAAAABaAFoAAAL+hI+py+0PY5i02mCupnnr7llgyAGkaJ6lurJYyo6nTNKh7eGb/sEqfwGiXC+isHJsxXwzZs15g+akO2rPaA1mh67kxFvsbpFj5a/8RYeX2LbYzX7L4/Qz3D7H15t3ft6/99Qn+EcYGDWIWKh4OJXoKBYhOUlZaXmJmamZ8FjVebUI2egZSjoKeqr1qVqKqvcKCGsoy0gramuK6xrLO9tb+3sbnDu863sMjCysTMxsnAy9HN08/Sx9TY1tnc297c2ayhVOtiquC35uXqy12e5uWU7eir6u7kx/b1+Nv6+vzf/PXzeAAwV+M0jwoLxxZuotTPfQYcN8ESlO7FcR48XJgBk5bizYEeRHhSMTmkSIMiTJNPFKpnSp8mTMlyzn0VwDEabOmgx55vQpEahFoVHeGT2KNKnSBi2JenQqEupKnEGpDrWqUarMnVifdo36dSqYsWrINg27VetNszZnuuXKtifatWXrno37c+5btXv1wrXb9u9dwHLxVjV8FXFWv3wFB06zNLK7wZQfM76s2GtmsJvFEs7bOS3mz4dJJza9ODTdyoVRa3bNGbZn1qBli1bdF7fj1rRL9z79O7Xt1ZZ1Nz7+QrJyTAUAADs='''
        self.gridimg=tk.PhotoImage(data=self.base)
        #Create label with the image, place into map frame
        self.panel = tk.Label(self.map, image=self.gridimg,anchor='w', justify='left')
        self.panel.grid(row=0)
        #Below function decodes base64 encoded player icon .gif
        self.base2='''R0lGODlhBwAHAPEAAAAAAP8AABkA/wAAACH5BAEAAAAALAAAAAAHAAcAAAIPBIJ2wnEhUJRUNgeRM9MUADs='''
        self.gridimg2=tk.PhotoImage(data=self.base2)
        #Create label with the player icon, place into map frame
        self.playericon = tk.Label(self.map, image=self.gridimg2,anchor='w', justify='left')
        self.x=40.5
        self.y=76.5
        #Uses place instead of grid, move in increments of 18
        self.playericon.place(x = self.x, y = self.y)


        #Create LabelFrame for stats, put into column 2 for bottomframe
        self.statbox = tk.LabelFrame(self.bottomframe,text="Stats",relief='ridge',labelanchor='n')
        self.statbox.grid(row=0, column=2, sticky=tk.W,padx=10)
        #Create Message for stats, put statbox
        self.statstr="HP: {}\nEnergy: {}\nEnemies Left: {}".format(player.health, player.energy, player.enemy)
        self.stats = tk.Message(self.statbox,text=self.statstr,width=100,justify='center')
        self.stats.grid()


        #Create LabelFrame for item list, put into column 3 for bottomframe
        self.items=tk.LabelFrame(self.bottomframe,text="Items",relief='ridge',labelanchor='n')
        self.items.grid(row=0, column=3, sticky=tk.W, padx=10)
        #Add ListBox for items
        self.itemlist=tk.Listbox(self.items,height=5)
        self.itemlist.grid(row=0)
        #Add Examine button for item
        self.examine=tk.Button(self.items,text="Examine",width=7)
        self.examine.grid(row=1,column=0,sticky='w')
        self.examine['command']=self.examineitem
        #Add Use button for item
        self.use=tk.Button(self.items,text="Use",width=7)
        self.use.grid(row=1,column=0,sticky='e')
        self.use['command']=self.useitem
        #Add each item to GUI list
        self.itemlist.insert(0,"Potions: "+str(player.inventory["Potion"]))
        self.itemlist.insert(1,"Haggis: "+str(player.inventory["Haggis"]))
        self.itemlist.insert(2,"Throwing Knives: "+str(player.inventory["Throwing Knife"]))


    #Function that enables the text widget to add text(dialogue) then re-disable it
    def gameprint(self, text,tag=None):
        self.dialogue.configure(state="normal")
        self.dialogue.insert(tk.END, text+"\n",tag)
        self.dialogue.configure(state="disabled")
        #This makes it auto scroll to bottom when dialogue box is updated
        self.dialogue.yview_moveto( 1 )


    #Refreshes display of user states to update it on the GUI, also checks for items and enemies
    def updateInfo(self):
        self.PickUp = True
        #Update GUI
        self.statstr="HP: {}\nEnergy: {}\nEnemies Left: {}".format(player.health, player.energy, player.enemy)
        self.stats.config(text=self.statstr)
        #Check if out of energy and haggis
        if player.energy < 1 and player.inventory["Haggis"] < 1:
            self.gameover()
        #Check for enemy
        for i in enemieslist:
            if player.x == i.x and player.y == i.y:
                self.enemyEncounter(i.level,i)
        #Check for items
        if self.PickUp == True:
            for i in [potion1,potion2,potion3,potion4,haggis1,haggis2,haggis3,haggis4,dagger1,dagger2,dagger3,dagger4]:
                if player.x == i.x and player.y == i.y:
                    self.gameprint("You found an item.",'item')
                    i.x = None
                    i.y = None
                    player.inventory[i.name] += 1
                    self.refresh()


    #Creates enemy encounter messagebox
    def enemyEncounter(self,level,enemy):
        self.enemyenc = enemy
        self.enemylevel = level
        self.msgwin = tk.Toplevel()
        self.msgwin.grab_set()
        self.msgwin.focus_force()
        self.msgwin.title("FIGHT")
        self.msgwin.protocol("WM_DELETE_WINDOW",self.disable_event)
        message = "Placeholder"
        label = tk.Label(self.msgwin,text="Enemy spotted! Will you engage them?")
        label.pack()
        ybutton = tk.Button(self.msgwin,text="Yes",command=self.enemyCombat)
        ybutton.pack()
        nbutton = tk.Button(self.msgwin,text="No",command=self.disengage)
        nbutton.pack()


    #Creates window with combat UI
    def enemyCombat(self):
        self.enemyenc.x = None
        self.enemyenc.y = None
        self.msgwin.grab_release()
        self.msgwin.destroy()
        self.cbtwin = tk.Toplevel(None,width="450",height="120")
        self.cbtwin.title("Enemy Combat Engaged")
        self.cbtwin.protocol("WM_DELETE_WINDOW",self.disable_event)
        self.cbtwin.pack_propagate(0)
        self.cbtwin.focus_force()
        self.cbtwin.grab_set()


        self.enemyhp = self.enemylevel


        self.label = tk.Label(self.cbtwin,text="Level "+str(self.enemylevel)+" enemy engaged."+'\n'+"Enemy Health: "+str(self.enemyhp)+'\n'+"Your Health: "+str(player.health))
        self.label.pack()


        self.fightbutton = tk.Button(self.cbtwin,text="Attack",command=self.diceRoll)
        self.fightbutton.pack()


        self.itembutton = tk.Button(self.cbtwin,text="Use Throwing Knife",command=self.throwingKnife)
        self.itembutton.pack()


    #Rolls dice if player chooses to fight, creates alert message about who won the turn
    def diceRoll(self):
        self.playerRoll = random.randrange(1,11)
        self.enemyRoll = random.randrange(1,11)


        if self.playerRoll == self.enemyRoll:
            player.health -= 1
            self.enemyhp -= 1
            tkm.showinfo(None,"You and the enemy countered each other's attacks!"+'\n'+"Both Rolls: "+str(self.playerRoll))
        elif self.playerRoll > self.enemyRoll:
            self.enemyhp -= 1
            tkm.showinfo(None,"You overcame the enemy's defenses!"+'\n'+"Roll: "+str(self.playerRoll)+'\n'+"Enemy: "+str(self.enemyRoll))
        else:
            player.health -= 1
            tkm.showinfo(None,"The enemy overcame your defenses!"+'\n'+"Roll: "+str(self.playerRoll)+'\n'+"Enemy: "+str(self.enemyRoll))
        #Refresh window message to reflect change in HP
        self.label.config(text="Level "+str(self.enemylevel)+" enemy engaged."+'\n'+"Enemy Health: "+str(self.enemyhp)+'\n'+"Your Health: "+str(player.health))
        self.checkbattle()


    #Check if player or enemy is at 0 HP
    def checkbattle(self):
        if player.health < 1:
            self.gameover()
        elif self.enemyhp < 1:
            self.winbattle()


    #When player wins battle, close the combat UI
    def winbattle(self):
        tkm.showinfo(None,"You've won the battle!")
        self.cbtwin.grab_release()
        self.cbtwin.destroy()
        player.enemy -= 1
        if player.enemy < 1:
            self.youwin()
    
    #Instant win battle when player uses throwing knife
    def throwingKnife(self):
        if player.inventory["Throwing Knife"] > 0:
            player.inventory["Throwing Knife"] -= 1
            tkm.showinfo(None,"You struck the enemy in its weak point with a throwing knife")
            self.winbattle()
            self.refresh()
        else:
            tkm.showinfo(None,"You have no throwing knives to use!")


    #Game over when player is out of health or out of energy and has no haggis
    def gameover(self):
        if player.health ==  0:
            tkm.showinfo(None,"You're out of HP. Game Over.")
        elif player.energy == 0 and player.inventory["Haggis"] == 0:
            tkm.showinfo(None,"You're out of energy and haggis. Game Over.")
        self.window.destroy()
        quit()


    #Player wins
    def youwin(self):
        tkm.showinfo(None, "The evil has been defeated. You win.")
        self.window.destroy()
        quit()


    #Empty function assigned to window close buttons in order to disable closing combat UI
    def disable_event(self):
        pass


    #Run away from the enemy. Expend 1 energy, do not pickup items
    def disengage(self):
        player.energy -= 1
        self.gameprint("You ran away from the enemy. One energy point used.")
        self.statstr="HP: {}\nEnergy: {}\nEnemies Left: {}".format(player.health, player.energy, player.enemy) #update energy
        self.stats.config(text=self.statstr) #update energy
        self.msgwin.destroy()
        self.PickUp = False


    #Refresh user inventory on GUI
    def refresh(self):
        self.itemlist.delete(0)
        self.itemlist.insert(0,"Potions: "+str(player.inventory["Potion"]))
        self.itemlist.delete(1)
        self.itemlist.insert(1,"Haggis: "+str(player.inventory["Haggis"]))
        self.itemlist.delete(2)
        self.itemlist.insert(2,"Throwing Knives: "+str(player.inventory["Throwing Knife"]))
    
    #Use item and deplete it from player inventory
    def useitem(self):
        if self.itemlist.curselection() == (0,):
            if player.inventory["Potion"] > 0:
                player.inventory["Potion"] = player.inventory["Potion"]-1
                self.gameprint("You restored your health!")
                player.health += 4
                if player.health > 15:
                    player.health = 15
            else:
                self.gameprint("You have no potions!")
        if self.itemlist.curselection() == (1,):
            if player.inventory["Haggis"] > 0:
                player.inventory["Haggis"] = player.inventory["Haggis"]-1
                self.gameprint("You restored energy!")
                player.energy += 7
                if player.energy > 10:
                    player.energy = 10
            else:
                self.gameprint("You have no haggis!")
        if self.itemlist.curselection() == (2,):
            if player.inventory["Throwing Knife"] > 0:
                self.gameprint("You can only use throwing knives during battle!")
            else:
                self.gameprint("You have no throwing knives!")
        self.updateInfo()
        self.refresh()


    #Examine item if it's in inventory
    def examineitem(self):
        if self.itemlist.curselection() == (0,) and player.inventory["Potion"] > 0:
            self.gameprint("Heals some health")
        elif self.itemlist.curselection() == (1,) and player.inventory["Haggis"] > 0:
            self.gameprint("Restores some energy")
        elif self.itemlist.curselection() == (2,) and player.inventory["Throwing Knife"] > 0:
            self.gameprint("Instantly win a battle")
        else:
            self.gameprint("You do not have this item")


    #Moves player position and also moves marker on the map
    def moveUp(self):
        if player.y < 5 and player.energy > 0:
            self.y -= 18
            self.playericon.place(x = self.x, y= self.y)
            player.y += 1
            player.energy -= 1
            self.swaproom()
            self.updateInfo()
        else:
            self.gameprint("You aren't able to do that.")
            if player.energy == 0:
                self.gameprint("You have no energy. Try eating a haggis.")
    def moveDown(self):
        if player.y > 1 and player.energy > 0:
            self.y += 18
            self.playericon.place(x = self.x, y= self.y)
            player.y -= 1
            player.energy -= 1
            self.swaproom()
            self.updateInfo()
        else:
            self.gameprint("You aren't able to do that.")
            if player.energy == 0:
                self.gameprint("You have no energy. Try eating a haggis.")
    def moveLeft(self):
        if player.x > 1 and player.energy > 0:
            self.x -= 18
            self.playericon.place(x = self.x, y= self.y)
            player.x -= 1
            player.energy -= 1
            self.swaproom()
            self.updateInfo()
        else:
            self.gameprint("You aren't able to do that.")
            if player.energy == 0:
                self.gameprint("You have no energy. Try eating a haggis.")
    def moveRight(self):
        if player.x < 5 and player.energy > 0:
            self.x += 18
            self.playericon.place(x = self.x, y= self.y)
            player.x += 1
            player.energy -= 1
            self.swaproom()
            self.updateInfo()
        else:
            self.gameprint("You aren't able to do that.")
            if player.energy == 0:
                self.gameprint("You have no energy. Try eating a haggis.")
    #Swap currentroom to match the player's coordinates and display the corresponding description
    def swaproom(self):
        if player.x==1 and player.y==1:
            self.currentroom=r11
        elif player.x==1 and player.y==2:
            self.currentroom=r12
        elif player.x==1 and player.y==3:
            self.currentroom=r13
        elif player.x==1 and player.y==4:
            self.currentroom=r14
        elif player.x==1 and player.y==5:
            self.currentroom=r15
        elif player.x==2 and player.y==1:
            self.currentroom=r21
        elif player.x==2 and player.y==2:
            self.currentroom=r22
        elif player.x==2 and player.y==3:
            self.currentroom=r23
        elif player.x==2 and player.y==4:
            self.currentroom=r24
        elif player.x==2 and player.y==5:
            self.currentroom=r25
        elif player.x==3 and player.y==1:
            self.currentroom=r31
        elif player.x==3 and player.y==2:
            self.currentroom=r32
        elif player.x==3 and player.y==3:
            self.currentroom=r33
        elif player.x==3 and player.y==4:
            self.currentroom=r34
        elif player.x==3 and player.y==5:
            self.currentroom=r35
        elif player.x==4 and player.y==1:
            self.currentroom=r41
        elif player.x==4 and player.y==2:
            self.currentroom=r42
        elif player.x==4 and player.y==3:
            self.currentroom=r43
        elif player.x==4 and player.y==4:
            self.currentroom=r44
        elif player.x==4 and player.y==5:
            self.currentroom=r45
        elif player.x==5 and player.y==1:
            self.currentroom=r51
        elif player.x==5 and player.y==2:
            self.currentroom=r52
        elif player.x==5 and player.y==3:
            self.currentroom=r53
        elif player.x==5 and player.y==4:
            self.currentroom=r54
        elif player.x==5 and player.y==5:
            self.currentroom=r55
        #Show description of room
        self.gameprint(self.currentroom.description,'desc')






#Room class to make each room an object with a random description
class Room:
    def __init__(self, roomid):
        self.roomid = roomid
        if self.roomid == 0:
            self.description="You have entered the lobby! A crystal chandelier illuminates the crimson carpet and marble floors."
        elif self.roomid == 1:
            self.description="You have entered a lounge! A velvet sofa and a bearskin rug sit atop the hardwood floors in the center of the room. A fire burns in the hearth."
        elif self.roomid == 2:
            self.description="You have entered a kitchen! The walls are lined with rustic wood cupboards and the refrigerator is left ajar in the corner."
        elif self.roomid==3:
            self.description="You have entered a bathroom! The bathroom is fluorescently lit and the tiles create a checkerboard pattern across the floor."
        elif self.roomid==4:
            self.description="You have entered a bedroom! Ambient light reflects through the linen drapes covering the terrace window."
        elif self.roomid==5:
            self.description= "You have entered a garden! The garden is in the courtyard of the building. There's a koi pond."
        elif self.roomid==6:
            self.description="You have entered a study! The bookshelves are stocked to the ceiling in this fully mahogany study. The room smells of burnt cigar tobacco."
        elif self.roomid==7:
            self.description="You have entered a basement! Cobwebs brush over your face as you enter the room. A washing machine rumbles away in the corner."
        elif self.roomid==8:
            self.description="You have entered a garage! There are wo parked cars: a cherry red, 1967 Chevrolet Camaro, and a black, 2017 Honda Civic Coupe."
        elif self.roomid==9:
            self.description="You have entered a studio!"
        elif self.roomid==10:
            self.description="You have entered a gym! Treadmill,  ellipticals, weight benches and barbells are scattered about."
        elif self.roomid==11:
            self.description= "You have entered an office! An iMac desktop computer is running. On the screen, Adobe Illustrator is open and sketches of logos and words are scribed on papers below."
        elif self.roomid==12:
            self.description="You have entered a terrace! The balcony overlooks the courtyard garden and on it are two metal chairs and a table."
        elif self.roomid==13:
            self.description="You have entered a living room! On the TV, an episode of The Simpsons is playing."
        elif self.roomid==14:
            self.description="You have entered a dining room!  A record player is quietly spinning John Lewis’ Afternoon In Paris."
        elif self.roomid==15:
            self.description="You have entered a laboratory! Notes and papers are scattered around the metal tables. On the shelves are beakers containing unidentified liquids."
        elif self.roomid==16:
            self.description="You have entered the roof! There is a patio set in the center and a series of satellites and antennae in the corners."
        elif self.roomid==17:
            self.description="You have entered a wine cellar! The all wood cellar holds 200 bottles of wine, sorted by origin, age, and color."
        elif self.roomid==18:
            self.description="You have entered a chapel! The room is no bigger than a closet. A cushion for visitors to kneel is placed before an icon of an unidentified deity."
        elif self.roomid==19:
            self.description="You have entered a wax figurine collection room! The room holds dozens of full scale wax figures."
        elif self.roomid==20:
            self.description="You have entered an echo chamber! The carefully placed sheets of metal cause any noises in the room to reverberate."
        elif self.roomid==21:
            self.description="You have entered a pantry! Dry and canned foods line the walls. The pantry does not contain any Doritos."
        elif self.roomid==22:
            self.description="You have entered a hanger! A Cessna 1721 Skyhawk aircraft is parked in front of the garage door that separates it from the runway."
        elif self.roomid==23:
            self.description="You have entered an art gallery! On the walls are original Picasso and Warhol pieces."
        elif self.roomid==24:
            self.description="You have entered a watchtower! The stone tower stands high above the building’s roof and overlooks the tri-state area."
        elif self.roomid==25:
            self.description="You have entered a portal! The portal transports you to a room in the Rolktar Dimension."
        elif self.roomid==26:
            self.description="You have entered an auditorium! The stage is equipped with lights and catwalks and the seating is arranged in an amphitheater style."
        elif self.roomid==27:
            self.description="You have entered a wave-pool! This natatorium is an exact replica of the wave-pool at the Kalahari Resort at Wisconsin Dells. Nobody is in the pool."
        elif self.roomid==28:
            self.description="You have entered the throne room! Nobody sits on the Iron Throne."
        elif self.roomid==29:
            self.description="You have entered a distillery! Inside the copper and steel tanks, hundreds of gallons of whiskey are in their second cycle of distillation."
        elif self.roomid==30:
            self.description="You have entered a crime scene! You crawl through barricades of yellow tape to enter the room. Shattered glass and items of evidence are littered around the floor."
        elif self.roomid==31:
            self.description="You have entered a barn! It smells of livestock. Cows moo and horses neigh when they hear you enter."
        elif self.roomid==32:
            self.description="You have entered a catacomb! The graves of elders past are stacked on top of each other on the walls, each with a statue of their face."
        elif self.roomid==33:
            self.description="You have entered a movie theater! The screen is playing the 2004 film Kill Bill Vol. 2."
        elif self.roomid==34:
            self.description="You have entered a solarium! The room has glass walls and ceilings that allow natural light to illuminate the city. "




#Player class for a player object to cotnrol
class Player:
        def __init__(self):
                self.health = 15
                self.energy = 10
                self.enemy = 17
                self.inventory = {"Potion":0, "Haggis":0, "Throwing Knife":0}
                self.x = 3
                self.y = 1


#Item class with three different types of items
class Item:
        def __init__(self,typeof,x,y):
            self.typeof = typeof
            self.x = x
            self.y = y
            if typeof == 1:
                self.name = "Potion"
            elif typeof == 2:
                self.name = "Haggis"
            elif typeof == 3:
                self.name = "Throwing Knife"


#Enemy class with varying levels
class Enemy:
    def __init__(self,x,y,level):
        self.x = x
        self.y = y
        self.level = level


#Generate player
player = Player()
#Generate game
game = Game()
#Generate items and randomize location
potion1 = Item(1,random.randrange(1,6),random.randrange(1,6))
potion2 = Item(1,random.randrange(1,6),random.randrange(1,6))
potion3 = Item(1,random.randrange(1,6),random.randrange(1,6))
potion4 = Item(1,random.randrange(1,6),random.randrange(1,6))
haggis1 = Item(2,random.randrange(1,6),random.randrange(1,6))
haggis2 = Item(2,random.randrange(1,6),random.randrange(1,6))
haggis3 = Item(2,random.randrange(1,6),random.randrange(1,6))
haggis4 = Item(2,random.randrange(1,6),random.randrange(1,6))
dagger1 = Item(3,random.randrange(1,6),random.randrange(1,6))
dagger2 = Item(3,random.randrange(1,6),random.randrange(1,6))
dagger3 = Item(3,random.randrange(1,6),random.randrange(1,6))
dagger4 = Item(3,random.randrange(1,6),random.randrange(1,6))
#Generate rooms and randomize descriptions
numberofrooms = 34
roomoptions=random.sample(range(34),25)
r11= Room(roomoptions[0])
r12= Room(roomoptions[1])
r13= Room(roomoptions[2])
r14= Room(roomoptions[3])
r15= Room(roomoptions[4])
r21= Room(roomoptions[5])
r22= Room(roomoptions[6])
r23= Room(roomoptions[7])
r24= Room(roomoptions[8])
r25= Room(roomoptions[9])
r31= Room(roomoptions[10])
r32= Room(roomoptions[11])
r33= Room(roomoptions[12])
r34= Room(roomoptions[13])
r35= Room(roomoptions[14])
r41= Room(roomoptions[15])
r42= Room(roomoptions[16])
r43= Room(roomoptions[17])
r44= Room(roomoptions[18])
r45= Room(roomoptions[19])
r51= Room(roomoptions[20])
r52= Room(roomoptions[21])
r53= Room(roomoptions[22])
r54= Room(roomoptions[23])
r55= Room(roomoptions[24])
#Generate enemies, randomize locations
enemiesxy=random.sample([[x, y] for x in range(1,6) for y in range(1,6)], 17)
enemieslist=[]
for i in range (0,7):
    enemieslist.append(Enemy(enemiesxy[i][0],enemiesxy[i][1],1))
for i in range (7,13):
    enemieslist.append(Enemy(enemiesxy[i][0],enemiesxy[i][1],2))
for i in range (13,17):
    enemieslist.append(Enemy(enemiesxy[i][0],enemiesxy[i][1],3))
#Call main function
main()