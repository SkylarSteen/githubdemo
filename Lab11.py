import matplotlib.pyplot as plt
import os
def estudiantes():
    students={}
    with open("data/students.txt") as file:
        for line in file:
            name=line[3:].strip()
            id=line[:3].strip()
            students[id]=name
    return students

def assignments_func():
    assignments={}
    with open("data/assignments.txt") as file:
        lines=file.readlines()
        for line in range(0,len(lines), 3 ):
            assign_name=lines[line].strip()
            assign_id=lines[line+1].strip()
            points = int(lines[line + 2].strip())
            assignments[assign_id]= (assign_name, points)
    return assignments

def submissions_func():
    submissions={}
    path="data/submissions"
    for file in os.listdir(path):
        filepath= os.path.join(path,file)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                for line in file:
                    id, assign_id, percentage=line.strip().split("|")
                    percentage= int(percentage.strip())

                    if assign_id not in submissions:
                        submissions[assign_id]=[]
                    submissions[assign_id].append((id,percentage))
    return submissions


def main():
    students = estudiantes()
    assignments = assignments_func()
    submissions = submissions_func()

    while True:
        print("""\n1. Student grade
        2. Assignment statistics
        3. Assignment graph""")


def student_grade(students, submissions, assignments):
    student_name = input("What is the student's name: ")
    student_id = None

    for id, name in students.items():
        if name.lower() == student_name.lower():
            student_id = id
            break

    if student_id:
        total_score = 0
        total_points = 0
        for assign_id, submissions_list in submissions.items():

            for s_id, score in submissions_list:
                if s_id == student_id:
                    assign_name, max_points = assignments.get(assign_id, (None, 0))
                    total_score += (score * max_points) / 100
                    total_points += max_points
                    break

        if total_points > 0:
            overall_grade = round((total_score / total_points) * 100)
            print(f"{overall_grade}%")
        else:
            print(f"{student_name} has no submissions.")
    else:
        print("Student not found.")




def assignment_statistics(submissions, assignments):
    assign_name = input("What is the assignment name: ")
    assign_id = None
    for id, (name, _) in assignments.items():
        if name.lower() == assign_name.lower():
            assign_id = id
            break

    if assign_id and assign_id in submissions:
        scores = [score for _, score in submissions[assign_id]]
        min_score = min(scores)
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        print(f"Assignment '{assign_name}' statistics:")
        print(f"Min: {round(min_score)}%")
        print(f"Avg: {round(avg_score)}%")
        print(f"Max: {round(max_score)}%")
    else:
        print("Assignment not found.")




def plot_assignment_scores(submissions, assignments, assign_id):
    assign_name, points = assignments[assign_id]
    scores = [score for _, score in submissions.get(assign_id, [])]
    plt.hist(scores, bins=[50, 55, 60,65,70,75,80,85,90,95,100])
    plt.title(f'Scores{assign_name}')
    plt.xlabel('Score Range (%)')
    plt.ylabel('# of Students')
    plt.show()




def assignment_graph(submissions, assignments):
    assign_name = input("What is the assignment name: ")
    assign_id = None
    for id, (name, _) in assignments.items():
        if name.lower() == assign_name.lower():
            assign_id = id
            break

    if assign_id and assign_id in submissions:
        plot_assignment_scores(submissions, assignments, assign_id)
    else:
        print("Assignment not found.")



def main():
    students = estudiantes()
    assignments = assignments_func()
    submissions = submissions_func()

    while True:
        print("""\n1. Student grade
2. Assignment statistics
3. Assignment graph""")

        choice = int(input("Enter your selection: "))
        if choice == 1:
            student_grade(students, submissions, assignments)
            break
        elif choice == 2:
            assignment_statistics(submissions, assignments)
            break
        elif choice == 3:
            assignment_graph(submissions, assignments)
            break


if __name__ == "__main__":
    main()