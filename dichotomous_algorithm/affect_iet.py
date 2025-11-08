# This algo use a dichotomous algorithm to assign students to their choices of postes
# It reads from a CSV file 'affectation.csv' where the first row contains student names and subsequent rows contain their choices.
# It also reads from 'poste_dispo.csv' to get the available postes and their counts.
# The algorithm randomly shuffles the students and their choices, then assigns postes based on the students' preferences and availability.


import csv
import random

import sys

log_file = open("results.log","w")
sys.stdout = log_file

postes = []

with open('affectation.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')  

    students = next(reader)[1:]

    student_choices = {student: [] for student in students}

    for row in reader:
        poste = row[0]
        postes.append(poste)
        for i, student in enumerate(students):
            if row[i+1] == '1':
                student_choices[student].append(poste)
        random.shuffle(student_choices[student])

# je devrais avoir une liste avec {student : [choice1, choice2, choice3]}
print(student_choices)

random.shuffle(postes)
random.shuffle(students)

print(postes)
print(students)

results = {}

for student in students:
    print(f"choosing for student {student} : with favorite choices {student_choices[student]} between available {postes}")
    # Je parcours les choix des etudiants et si j'arrive a retirer le poste aux postes disponibles je passe a l'etudiant suivant
    if not any(choice in postes for choice in student_choices[student]):
        print(f"No available choices for student {student} among remaining postes")
        continue
    else:
        results[student] = postes.pop()
        print(f"Student {student} has been assigned to {results[student]}")
        students.remove(student)


print(f"Les etudiants n'ont pas eu d'affectations : {students}")

print(f"Nouvelle itéaration avec les postes restants : {postes}")
for student in students:
    available = postes.pop()
    results[student] = available;
    print(f"Student {student} has been assigned to {available}")

print(f"Results are : {results}")

with open('result_affectation.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Student', 'Assigned Poste'])
    for student, poste in results.items():
        writer.writerow([student, poste])

log_file.close()
