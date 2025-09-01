
import csv


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

# J'ai une liste de postes par etudiant ordonnée par priorité
# chaque étudiant "mange" son poste préféré encore disponible à chaque itération
# si plusieurs étudiants veulent le même poste, ils le mangent à part égale

# Le restulat est une liste des etudiants avec pour chacun la liste des postes et la part correspondante
results: dict[str, dict[str, float]] = {}

max_iterations = len(postes_disponibles) * 10  
iteration_count = 0

# J'initie la capacité restante de chaque poste à 1
postes_remaining_capacity = {poste: 1 for poste in postes_disponibles}

while postes_disponibles:
    iteration_count += 1
    if iteration_count > max_iterations:
        print("Error: Infinite loop detected. Exiting.")
        break

    # je crée un dictionnaire avec pour chaque poste les etudiants branchés actuellement 
    postes_currently_eaten_by = {poste: [] for poste in postes_disponibles}
    

    # je parcours les choix des etudiants et les branche au poste qu'ils préfèrent
    for student_name, student_choice in student_choices_ordered.items():
            # je dois brancher l'étudiant au poste qu'il préfère encore disponible
            # je prend le premier poste qui est encore dans postes_disponibles dans sa liste de choix ordonnée
            while student_choice and student_choice[0] not in postes_disponibles:
                student_choice.pop(0)

            if not student_choice or len(student_choice) == 0:
                continue

            available_choice = student_choice[0]            
            
            postes_currently_eaten_by[available_choice].append(student_name)
            print(f"{student_name} is eating {available_choice}")
    
    print(postes_currently_eaten_by)

    # je dois recuperer le temps_min c'est a dire le remaining_capacity / affluence le plus faible pour les postes 
    affluence_par_poste = [len(students) for poste, students in postes_currently_eaten_by.items() if postes_remaining_capacity[poste] > 0]
    capacity_by_poste = [capacity for poste, capacity in postes_remaining_capacity.items() if capacity > 0]
    # dans temps je veux obtenir une nouvelle liste avec pour chaque poste le remaining_capacity / affluence
    
    temps = [capacity / affluence if affluence > 0 else float('inf') 
             for capacity, affluence in zip(capacity_by_poste, affluence_par_poste)]

    temps_min = min(temps)

    for poste, students_eating in postes_currently_eaten_by.items():
        num_students_eating = len(students_eating)
        
        if num_students_eating > 0:
            postes_remaining_capacity[poste] -= temps_min * num_students_eating

        # j'ajoute la part mangé pour chaque étudiant dans le résultat
        for student in students_eating:
            if student not in results:
                results[student] = {}
            if (results[student].get(poste) is None):
                results[student][poste] = 0
            results[student][poste] += temps_min
        
        print(results)

        if postes_remaining_capacity[poste] <= 0:
            postes_disponibles.remove(poste)
            print(f"{poste} à été complètement mangé et est retiré des postes disponibles.")

    for student, postes_attribution in results.items():
        for poste in postes_attribution.keys():
            postes_attribution[poste] = round(postes_attribution[poste], 4)
            

    with open('resultats.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        # J'initie les en-têtes du fichier CSV
        header = ['IET'] + list(postes_remaining_capacity.keys())
        writer.writerow(header)

        for student, postes in results.items():
            row = [student]
            for poste in postes_remaining_capacity.keys():
                row.append(postes.get(poste, 0))  # 0 en valeur par défaut si le poste n'a pas été mangé par l'étudiant
            writer.writerow(row)
    
    print(postes_remaining_capacity)