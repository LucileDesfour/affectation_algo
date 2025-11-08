
import csv
import sys
import random

log_file = open("results.log","w")
sys.stdout = log_file

with open('IET.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  

    moderators = {}
    for row in reader:
        if len(row) >= 4:  
            name = row[0]
            moderators[name] = {
                'volunteer': int(row[1]),
                'gender': row[2],
                'groups': row[3].split(',')
            }

moderator_items = list(moderators.items())
random.shuffle(moderator_items)
moderators = dict(moderator_items)

with open('groupes.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    
    sous_groupes = {}
    for row in reader:
        if len(row) >= 3:  
            sous_groupe = row[0]
            sous_groupes[sous_groupe] = {
                'groupe': int(row[1]),
                'nb_postes': int(row[2])
            }

# Assign moderators to subgroups
assignments = {}

for sous_groupe, details in sous_groupes.items():
    
    gender = "M"
    nb_posts = details['nb_postes']
    groupe = details['groupe']
    
    # Determine number of moderators needed
    if nb_posts < 5:
        nb_mods_needed = 1
    elif 5 <= nb_posts <= 20:
        nb_mods_needed = 2
    else:
        nb_mods_needed = 3
        

    # Eligible moderators are those who are not in the same groupe as the sub groupe and are not already assigned
    eligible_mods = {
        name: mod for name, mod in moderators.items()
        if str(groupe) not in mod['groups'] and name not in [m for mods in assignments.values() for m in mods]
    }

    print(f"Sous groupe {sous_groupe} (groupe {groupe}) a besoin de {nb_mods_needed} moderateurs. Eligible: {list(eligible_mods.keys())}")
    
    # Prioritize volunteers
    volunteers = {n: m for n, m in eligible_mods.items() if m['volunteer'] == 1}
    
    print(f"Les volontaires disponibles pour ce sous groupe sont : {list(volunteers.keys())}")
    # Select moderators
    selected_mods = []
    last_gender = None

    def pick_next_mod(candidates, selected, needed_gender):
        for name, mod in candidates.items():
            if name not in selected and mod['gender'] == needed_gender:
                return name
        return None

    # Try to alternate genders, starting with 'M'
    genders = ['M', 'F']
    gender_idx = 0

    while len(selected_mods) < nb_mods_needed:
        needed_gender = genders[gender_idx % 2]
        print(f"Besoin d'un moderateur de genre {needed_gender}")
        # Try to pick from volunteers first
        name = pick_next_mod(volunteers, selected_mods, needed_gender)
        print(f"Moderateur choisi parmi les volontaires: {name}")
        if name is None:
            # If not available, pick from eligible_mods
            name = pick_next_mod(eligible_mods, selected_mods, needed_gender)
            print(f"Moderateur choisi parmi les eligibles: {name}")
        if name is None:
            # If still not available, pick any remaining eligible mod
            for n in eligible_mods:
                if n not in selected_mods:
                    name = n
                    print(f"Moderateur choisi parmi les restants: {name}")
                    break
        if name is None:
            break  # No more moderators available
        selected_mods.append(name)
        gender_idx += 1

    assignments[sous_groupe] = selected_mods

print("Moderator assignments:")
for sg, mods in assignments.items():
    print(f"{sg}: {mods}")

with open('result_moderator_assignment.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Sous-groupe', 'Assigned Moderators'])
    for sg, mods in assignments.items():
        writer.writerow([sg] + mods)

log_file.close()