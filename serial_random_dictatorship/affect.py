
import csv
import random


with open('affectation.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')  

    students = next(reader)[1:]

    student_choices = {student: [] for student in students}
    student_choices_ordered = {student: [] for student in students}

    postes_disponibles = []

    # Je creée une premiere liste avec pour chaque étudiant la liste de ses postes avec la priorité associée
    for row in reader:
        poste = row[0]
        for i, student in enumerate(students):
            priority = row[i+1]
            if priority != '0' and priority != '':
                student_choices[student].append((int(priority), poste))

        postes_disponibles.append(poste)

    print(student_choices)
    # J'ordonne la liste des postes par étudiants avec l'ordre de priorité définit
    for student in students:
        sorted_postes = sorted(student_choices[student])  
        student_choices_ordered[student] = [poste for _, poste in sorted_postes]


print(student_choices_ordered)
print(postes_disponibles)


student_random_order = list(student_choices_ordered.keys())
# J'ordonne la liste des étudiants par ordre aléatoire
random.shuffle(student_random_order)
# J'ordonne la liste des postes disponibles par ordre aléatoire pour les édutiants qui n'obtiendront aucun de leur choix ordonné
random.shuffle(postes_disponibles)

results = {}

for student in student_random_order:
    print(f"choosing for student {student} between {postes_disponibles}")
    print(f"ordered choices: {student_choices_ordered[student]}")
    for poste in student_choices_ordered[student]:
        if poste in postes_disponibles:
            results[student] = poste
            postes_disponibles.remove(poste)
            break
    if (student not in results):
        results[student] = postes_disponibles.pop(0)  # J'assigne le premier poste disponible si aucun des choix n'est disponible

print("Results:")
for student, poste in results.items():
    print(f"{student} -> {poste}")