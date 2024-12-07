import random
import time
def spaceMaker(numOfSpaces):
    for i in range(numOfSpaces):
        print("")

def start_game(): 
    for i in range(10):
        print("")
    print("Welcome to the Python Adventure!")
    print("You are about to embark on a perilous journey...")
    
def create_character():
    name = input("Enter your character's name: ")
    userminions = 50
    usersHealth = 50
    spaceMaker(2)
    print("Choose your class:")
    print("1. warrior")
    print("2. wizzard")
    print("3. monkey")
    class_choice = input("Enter the the class of your choise: ").lower()
    spaceMaker(2)
    
    
    if class_choice == 'warrior':
        userMinions = 100
        usersHealth = 75
    elif class_choice == 'wizzard':
        userMinions = 50
        usersHealth = 125
    elif class_choice == 'monkey':
        userMinions = 75
        usersHealth = 100
    
    # ... implement class selection logic
    return {"name": name, "class": class_choice, "health": usersHealth, "minions": userMinions}

def display_status(character):
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Health: {character['health']}")
    print(f"minions:  {character['minions']}")
    spaceMaker(1)
    
    #add discription of each ability
    
    
def encounter_monster():
    monsters = ["Goblin", "Orc", "Troll", "Dragon"]
    monster = random.choice(monsters)
    minions = random.randint(1, 100)
    return monster, minions

def roundBattle(character, monster, roundNum):
    #PROBLEM: DOESN'T SAVE AMOUNT OF MONSTER MINIONS LEFT
    monster_name, monster_minions = monster
    attackingMinions = int(input(f"Input the number how many of your {character['minions']} minions you want to send over on the {roundNum + 1} round: "))
    attackingEnemyMinions = monster_minions - (monster_minions * (random.randrange(50, 75) / 100))
    
    spaceMaker(1)
    print(f"You sent over {attackingMinions}")
    print(f"{monster_name} sent over {attackingEnemyMinions}")
    time.sleep(2)
    
    character['minions'] -= attackingMinions
    
    monster_minions -= attackingEnemyMinions
    
    if attackingMinions <= attackingEnemyMinions:    
        time.sleep(1)
        print(f"Oof, {monster_name} won the {roundNum + 1} round, {monster_name} has {monster_minions} minions left")
        print(f"You have {character["minions"]} left")
        
        return False
    else:
        print(f"Congrats, You beat {monster_name} in the {roundNum + 1} round, {monster_name} has {monster_minions} minions left")
        print(f"You have {character["minions"]} left")
        time.sleep(2)
        return True
    
    
def battle(character, monster):
        # Implement battle logic
    numOfRoundsWonUser = 0
    numOfRoundsWonMonster = 0
    
    monster_name, monster_minions = monster
    
    print(f"Your about to battle {monster_name}, there will be 5 rounds")
    time.sleep(2)
    print("You and the monster will send a number of minions to battle out, the bieng that sent the most minions that round wins")
    time.sleep(2)
    print("But conserve your minions, as you only have the amount you already have, best of 5, good luck my friend!")
    time.sleep(2)
    
    tempMinionCount = character['minions']
    
    for i in range(3):
        # ROUNDBATTLE NEEDS TO SEND OVER AMOUNT OF MINIONS LEFT AFTER EACH BATTLE
        if roundBattle(character, monster, i):
            numOfRoundsWonUser += 1
            
        else:
            numOfRoundsWonMonster += 1
            
    character['minions'] = tempMinionCount
    
    if numOfRoundsWonUser > numOfRoundsWonMonster:
        character['minions'] += 10
        print("Congrats you won the battle")
        time.sleep(5)
    else:
        print("You lost the battle")
        time.sleep(5)
    
    # if character['minions'] <= monster_minions:
    #     # Subtract monster's minions from character's health
    #     character['health'] -= monster_minions
    #     print("You lost the fight")
    #     time.sleep(2)
    #     print(f"The monster {monster_name} is too strong! Your health is now {character['health']}.")
    #     time.sleep(4)
    #     # Return False if the character loses the battle (minions too low)
    #     if character['minions'] <= 0:
    #         return False
    # else:
    #     print(f"You defeated the {monster_name}!")
    #     time.sleep(1)
    #     print("Your minions has been increased by 10")
    #     character['minions'] += 5
    #     return True
        
def fightingMonster(character):
    monster, minions = encounter_monster()
    print(f"You encountered a {monster} with minions {minions}!")
    
    choiseFight = input(f"Do you want to fight the {monster} (1)? or do you want to take a chance and run (2)? ")
    spaceMaker(1)
    
    if choiseFight == '1':
        battle(character, (monster, minions))
    else:
        if random.randint(1, 2) == 1:
            print("You succesfully ran away")
            time.sleep(3)
        else:
            character['health'] -= minions/2
            print(f"You Tried running, but the {monster} caught up to you and delt you damage")
            time.sleep(2)
            print(f"you are now at {character['health']} health")
            time.sleep(4)
    


def find_treasure():
    items = ["Gold Coin", "Magic Potion", "Ancient Artifact"]
    item = random.choice(items)
    value = random.randint(1, 150)
    return item, value

def game_over(character):
    print("\nGame Over!")

    display_status(character)
    
def main():
    start_game()
    character = create_character()
    
    while character['health'] > 0:
        
        spaceMaker(2)
        
        print("Your stats are:")
        display_status(character)
        
        spaceMaker(1)
        choice = input("Do you want to (1) Look for monsters or (2) Search for treasure or (3) end your session? ")
        spaceMaker(1)
        
        if choice == '1':
            fightingMonster(character)
        elif choice == '2':
            item, value = find_treasure()
            print(f"You found a {item} worth {value} gold!")
        elif choice == '3':
            return
        else:
            print("Invalid choice. Try again.")
            game_over(character)
        # if __name__ == "__main__":
        #     main()
    else:
        print("You died")
        print(f"Your final stats are:")
        display_status(character)
main()