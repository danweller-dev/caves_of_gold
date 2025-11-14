# =========================================
#  CAVES OF GOLD – ITEMS MUST BE FOUND
#  (NO FUNCTIONS VERSION)
# =========================================

import random   # randomness

print("\n===================================")
print("       WELCOME TO CAVES OF GOLD")
print("===================================\n")
print("Explore the dungeon, fight monsters,")
print("find treasure and try to stay alive!\n")

name = input("Adventurer, what is your name? ")
print("\nGood luck,", name + "!")
print("You enter the caves with only a simple stick...\n")

# Player stats
max_hp = 40
hp = max_hp
gold = 0
battles_won = 0     # counter

# START GEAR – very basic
current_weapon = "Wooden Stick"
weapon_bonus = 1

current_equipment = "No armour"
defence_bonus = 0

# Potions (start with none – must be found or won)
potion_heal = 0
potion_power = 0
potion_escape = 0

power_active = False      # Booleans
escape_ready = False
playing = True

# Weapons and equipment that can be found (3 of each)
weapon_names = ["Rusty Sword", "Hunter's Bow", "War Hammer"]
weapon_bonus_list = [3, 2, 4]

equipment_names = ["Leather Armour", "Iron Shield", "Lucky Charm"]
equipment_bonus_list = [1, 2, 0]

# Monsters (three types)
monster_names = ["Goblin", "Skeleton", "Ogre"]
monster_hp_list = [15, 20, 30]
monster_attack_min = [2, 3, 4]
monster_attack_max = [5, 6, 8]

turns = 0

# ============ MAIN GAME LOOP ============

while playing and hp > 0:
    turns = turns + 1

    # --- STATUS BLOCK ---
    print("\n-----------------------------------")
    print("TURN:", turns)
    print("HP:", hp, "/", max_hp)
    print("Gold:", gold)
    print("Weapon:", current_weapon, "(bonus +", weapon_bonus, ")")
    print("Equipment:", current_equipment, "(defence +", defence_bonus, ")")
    print("Potions -> Heal:", potion_heal,
          " Power:", potion_power,
          " Escape:", potion_escape)
    print("Battles won:", battles_won)
    print("-----------------------------------\n")

    print("What will you do?")
    print("  (E)xplore")
    print("  (R)est")
    print("  use (P)otion")
    print("  (Q)uit\n")
    choice = input("Your choice: ").lower()
    print()

    # ---------- EXPLORE ----------
    if choice == "e":
        print("You move deeper into the caves...\n")
        event_roll = random.randint(1, 100)

        # 1–40: monster, 41–60: gold, 61–75: trap, 76–85: item, 86–100: nothing
        # MONSTER ENCOUNTER
        if event_roll <= 40:
            index = random.randint(0, 2)
            monster_name = monster_names[index]
            monster_hp = monster_hp_list[index]
            monster_min = monster_attack_min[index]
            monster_max = monster_attack_max[index]

            print("A wild", monster_name, "appears!\n")

            # COMBAT LOOP
            while hp > 0 and monster_hp > 0 and playing:
                print("===================================")
                print(name, "HP:", hp, "/", max_hp,
                      "   |   ", monster_name, "HP:", monster_hp)
                print("===================================\n")
                action = input("(A)ttack, (P)otion, (R)un: ").lower()
                print()

                # use potion (same menu as outside combat)
                if action == "p":
                    print("Potions:")
                    print("  1. Healing Potion")
                    print("  2. Power Potion")
                    print("  3. Escape Potion\n")
                    pot_choice = input("Choose 1, 2 or 3 (or anything else to cancel): ")
                    print()

                    if pot_choice == "1":
                        if potion_heal > 0:
                            potion_heal = potion_heal - 1
                            heal = random.randint(10, 18)
                            hp = hp + heal
                            if hp > max_hp:
                                hp = max_hp
                            print("You drink a Healing Potion and recover", heal, "HP.\n")
                        else:
                            print("You have no Healing Potions left.\n")
                    elif pot_choice == "2":
                        if potion_power > 0:
                            potion_power = potion_power - 1
                            power_active = True
                            print("You feel a surge of strength!\n")
                        else:
                            print("You have no Power Potions left.\n")
                    elif pot_choice == "3":
                        if potion_escape > 0:
                            potion_escape = potion_escape - 1
                            escape_ready = True
                            print("You will automatically escape if you try to run.\n")
                        else:
                            print("You have no Escape Potions left.\n")
                    else:
                        print("You put your potions away.\n")
                    continue   # back to top of combat loop

                # try to run away
                if action == "r":
                    if escape_ready:
                        print("Your Escape magic whisks you away!\n")
                        escape_ready = False
                        break
                    else:
                        if random.random() < 0.5:
                            print("You manage to flee from the battle.\n")
                            break
                        else:
                            print("You fail to escape!\n")
                            # monster will attack below

                # attack (default if input is not recognised)
                if action == "a" or (action != "r" and action != "p"):
                    base = random.randint(3, 7)
                    damage = base + weapon_bonus
                    if power_active:
                        damage = damage + 4
                        power_active = False
                        print("Your Power Potion boosts your strike!\n")
                    monster_hp = monster_hp - damage
                    print("You hit the", monster_name, "for", damage, "damage.\n")

                # check if monster is defeated
                if monster_hp <= 0:
                    print("You defeated the", monster_name, "!\n")
                    battles_won = battles_won + 1

                    # treasure reward
                    reward = random.randint(8, 25)
                    gold = gold + reward
                    print("You loot", reward, "gold from the body.\n")

                    # chance of extra potion
                    loot_roll = random.randint(1, 100)
                    if loot_roll <= 25:
                        potion_heal = potion_heal + 1
                        print("You also find a Healing Potion.\n")
                    elif loot_roll <= 40:
                        potion_power = potion_power + 1
                        print("You also find a Power Potion.\n")
                    elif loot_roll <= 50:
                        potion_escape = potion_escape + 1
                        print("You also find an Escape Potion.\n")
                    break

                # monster attacks back
                damage = random.randint(monster_min, monster_max) - defence_bonus
                if damage < 1:
                    damage = 1
                hp = hp - damage
                print("The", monster_name, "hits you for", damage, "damage!\n")

                if hp <= 0:
                    print("You collapse to the dungeon floor...\n")
                    playing = False

        # TREASURE (gold only)
        elif event_roll <= 60:
            amount = random.randint(5, 20) + battles_won
            gold = gold + amount
            print("You find a small chest containing", amount, "gold!\n")

        # TRAP
        elif event_roll <= 75:
            print("A hidden trap springs from the floor!\n")
            base_damage = random.randint(4, 10)

            if current_equipment == "Lucky Charm":
                damage = base_damage // 2
                print("Your Lucky Charm glows and softens the blow.\n")
            elif current_equipment == "Iron Shield":
                damage = base_damage - 2
            else:
                damage = base_damage

            if damage < 1:
                damage = 1
            hp = hp - damage
            print("The trap hits you for", damage, "damage.\n")

            if gold > 0 and random.random() < 0.4:
                lost = random.randint(1, 5)
                if lost > gold:
                    lost = gold
                gold = gold - lost
                print("In the chaos you drop", lost, "gold!\n")

        # ITEM FIND – weapon, equipment or potion
        elif event_roll <= 85:
            print("You spot something interesting among the rocks...\n")
            item_roll = random.randint(1, 100)

            # 1–40: weapon, 41–80: equipment, 81–100: potion
            if item_roll <= 40:
                # weapon
                w_index = random.randint(0, 2)
                new_name = weapon_names[w_index]
                new_bonus = weapon_bonus_list[w_index]
                print("You find a", new_name, "(attack bonus +", new_bonus, ").\n")
                if new_bonus > weapon_bonus:
                    take = input("It is better than your current weapon. Take it? (y/n): ").lower()
                    print()
                    if take == "y":
                        current_weapon = new_name
                        weapon_bonus = new_bonus
                        print("You equip the", new_name + ".\n")
                    else:
                        print("You leave the weapon where it lies.\n")
                else:
                    print("It is worse than what you already have. You leave it.\n")

            elif item_roll <= 80:
                # equipment
                e_index = random.randint(0, 2)
                new_name = equipment_names[e_index]
                new_bonus = equipment_bonus_list[e_index]
                print("You find", new_name, "(defence +", new_bonus, ").\n")
                if new_bonus > defence_bonus:
                    take = input("It is better than your current equipment. Wear it? (y/n): ").lower()
                    print()
                    if take == "y":
                        current_equipment = new_name
                        defence_bonus = new_bonus
                        print("You change into", new_name + ".\n")
                    else:
                        print("You leave the equipment where it is.\n")
                else:
                    print("It is worse than what you already have. You leave it.\n")

            else:
                # potion find
                print("You find a dusty belt full of bottles.\n")
                pot_roll = random.randint(1, 3)
                if pot_roll == 1:
                    potion_heal = potion_heal + 1
                    print("You gain a Healing Potion.\n")
                elif pot_roll == 2:
                    potion_power = potion_power + 1
                    print("You gain a Power Potion.\n")
                else:
                    potion_escape = potion_escape + 1
                    print("You gain an Escape Potion.\n")

        else:
            print("Nothing happens... the cave is eerily quiet.\n")

    # ---------- REST (risk + healing) ----------
    elif choice == "r":
        print("You decide to rest for a while...\n")
        roll = random.randint(1, 100)
        if roll <= 70:
            heal = random.randint(5, 12)
            hp = hp + heal
            if hp > max_hp:
                hp = max_hp
            print("You feel better and recover", heal, "HP.\n")
        else:
            print("A trap triggers while you rest!\n")
            base_damage = random.randint(4, 10)
            if current_equipment == "Lucky Charm":
                damage = base_damage // 2
                print("Your Lucky Charm glows and softens the blow.\n")
            elif current_equipment == "Iron Shield":
                damage = base_damage - 2
            else:
                damage = base_damage
            if damage < 1:
                damage = 1
            hp = hp - damage
            print("The trap hits you for", damage, "damage.\n")

    # ---------- POTIONS OUTSIDE BATTLE ----------
    elif choice == "p":
        print("Potions:")
        print("  1. Healing Potion")
        print("  2. Power Potion")
        print("  3. Escape Potion\n")
        pot_choice = input("Choose 1, 2 or 3 (or anything else to cancel): ")
        print()

        if pot_choice == "1":
            if potion_heal > 0:
                potion_heal = potion_heal - 1
                heal = random.randint(10, 18)
                hp = hp + heal
                if hp > max_hp:
                    hp = max_hp
                print("You drink a Healing Potion and recover", heal, "HP.\n")
            else:
                print("You have no Healing Potions left.\n")
        elif pot_choice == "2":
            if potion_power > 0:
                potion_power = potion_power - 1
                power_active = True
                print("You feel a surge of strength! Your next attacks are stronger.\n")
            else:
                print("You have no Power Potions left.\n")
        elif pot_choice == "3":
            if potion_escape > 0:
                potion_escape = potion_escape - 1
                escape_ready = True
                print("You will automatically escape if you try to run from a battle.\n")
            else:
                print("You have no Escape Potions left.\n")
        else:
            print("You put your potions away.\n")

    # ---------- QUIT ----------
    elif choice == "q":
        playing = False
        print("You decide to leave the caves for now.\n")

    else:
        print("You hesitate, doing nothing...\n")

# ============ GAME OVER ============

print("\n===== GAME OVER =====")
print("Adventurer:", name)
print("Turns survived:", turns)
print("Battles won:", battles_won)
print("Total gold collected:", gold)
print("Thanks for playing CAVES OF GOLD!\n")
