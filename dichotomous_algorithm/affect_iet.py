# This algo use a dichotomous algorithm to assign students to their choices of postes
# It reads from a CSV file 'affectation.csv' where the first row contains student names and subsequent rows contain their choices.
# It also reads from 'poste_dispo.csv' to get the available postes and their counts.
# The algorithm randomly shuffles the students and their choices, then assigns postes based on the students' preferences and availability.


import csv
import random


with open('affectation.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')  

    students = next(reader)[1:]

    student_choices = {student: [] for student in students}

    for row in reader:
        poste = row[0]
        for i, student in enumerate(students):
            if row[i+1] == '1':
                student_choices[student].append(poste)
        random.shuffle(student_choices[student])


print(student_choices)
# je devrais avoir une liste avec {student : [choice1, choice2, choice3]}

# Ordonner dans un ordre aléatoire les étudiants

# Recuperer la liste de poste dans poste_dispo.csv 
# Dupliquer les postes en fonction du nombre de poste dispo 

with open('poste_dispo.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')  
    postes_dispo = {}

    next(reader)
    for row in reader:
        print(row)
        postes_dispo[row[0]] = int(row[1])


postes = []

for poste, nombre in postes_dispo.items():
    while nombre > 0:
        postes.append(poste)        
        nombre -= 1

random.shuffle(postes)
random.shuffle(students)

print(postes)
print(students)

results = {}

for student in students:
    print(f"choosing for student {student} : between choices {student_choices[student]} and available {postes}")
    # Je parcours les choix des etudiants et si j'arrive a retirer le poste aux postes disponibles je passe a l'etudiant suivant
    for choice in (student_choices[student]):
        try:
            postes.remove(choice)
            results[student] = choice;
            students.remove(student)
            print(f"Student {student} has been assigned to {choice}")
            break;
        except ValueError:
            continue;

print(f"Les etudiants suivants n'ont eu aucun de leurs choix : {students}")

print(f"Nouvelle itéaration avec les postes restants : {postes}")
for student in students:
    available = postes.pop()
    results[student] = available;
    print(f"Student {student} has been assigned to {available}")

print(f"Results are : {results}")