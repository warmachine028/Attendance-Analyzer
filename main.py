import os
import statistics

import matplotlib.pyplot as plt
import pandas

from data.csv_converter import Converter

CSV_PATH = 'data/student_attendance.csv'
PDF_PATH = 'data/student_attendance.pdf'


def converted():
    return os.path.isfile(CSV_PATH)


def display_choice():
    print(*(
        "",
        " 0. Exit",
        " 1. View All Student Records",
        " 2. View particular student Record with FULL NAME",
        " 3. View Student record with maximum % of Attendance",
        " 4. View Student record with minimum % of Attendance",
        " 5. View Student records with % of Attendance below 50%",
        " 6. View Student records with % of Attendance below 20%",
        " 7. View Attendance Statistics",
        " 8. Scatter Plot Attendance Records",
        " 9. Plot Attendance Records Segment wise",
        "10. Pie Chart Representation",
        "11. Standard Deviation/Bell Curve of this Record"
    ), sep='\n')


def fetch_segments(_df):
    _att = _df[Att]
    return ((_df[_att <= 20], _df.index[_att <= 20]),
            (_df[(20 < _att) & (_att < 50)], _df.index[(20 < _att) & (_att < 50)]),
            (_df[(50 < _att) & (_att < 70)], _df.index[(50 < _att) & (_att < 70)]),
            (_df[(70 < _att) & (_att < 85)], _df.index[(70 < _att) & (_att < 85)]),
            (_df[_att >= 85], _df.index[_att >= 85]))


def pie_plot():
    plt.figure(figsize=(10, 4))
    plt.title('Percentage wise analysis of Attendance Records for 2nd Year 2020 - 2024')
    group_names = fetch_labels()
    segments = fetch_segments(df)[::-1]
    counts = pandas.Series(map(lambda item: len(item[0][Att]), segments),
                           index=('>84 %', '70-84 %', '50-69 %', '20-49 %', '<20 %'), )
    explode = (0, 0, 0.2, 0.4, 0.6)[:5]
    colors = "mediumorchid", "teal", "slategray", "lightcoral", "darksalmon"

    counts.plot(kind='pie', fontsize=10, colors=colors, explode=explode, autopct=lambda pct: f"{pct:.2f}%")
    plt.ylabel('')
    plt.xlabel('OUTSIDE PIE: ATTENDANCE RANGE       INSIDE PIE: % OF STUDENTS IN THAT RANGE')
    plt.axis('equal')
    plt.legend(labels=group_names, loc='best')
    plt.show()


def bar_plot():
    ax = plt.subplots(figsize=(10, 4))[-1]
    plt.title('Quantitative analysis of Attendance Records for 2nd Year 2020 - 2024')
    plt.xlabel('Number of Students')
    plt.ylabel('Attendance Percentage Ranges')
    x_val = [len(item[0][Att]) for item in fetch_segments(df)[::-1]]
    y_ticks = '>84 %', '70-84 %', '50-69 %', '20-49 %', '<20 %'
    for i, (label, color) in enumerate(zip(fetch_labels(), fetch_colours())):
        ax.barh(y_ticks[i], x_val[i], label=label, color=color)
    for i, value in enumerate(x_val):
        ax.text(value - 40, i - 0.15, str(value), color='black', fontsize=13)
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()


def scatter_plot():
    plt.figure(figsize=(10, 4))
    plt.title('Scattering Attendance Records for 2nd Year Batch 2020 - 2024')
    plt.xlabel('Number of Students')
    plt.ylabel('% of Attendance')
    colours = iter(fetch_colours())
    labels = iter(fetch_labels())
    for item in fetch_segments(df)[::-1]:
        plt.scatter(list(item[1]), list(item[0][Att]), label=next(labels), color=next(colours))
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()


def line_plot():
    print("COMMING SOON")


def fetch_colours():
    return 'g', 'lightgreen', 'blue', 'magenta', 'r'


def fetch_labels():
    return 'Best', 'Good', 'Fair', 'Need to Improve', 'Danger'


# __main__
print("Welcome to Student Attendance Analyzer")
if not converted():
    print(*(
        "WARNING! CSV FILE NOT FOUND IN DIRECTORY",
        "CONVERTING PDF FILE TO CSV..",
        "IT WILL TAKE SOME TIME",
        "THE PROGRAM ISN'T STUCK"
    ), sep='\n')
    Converter(PDF_PATH, CSV_PATH).convert()

df = pandas.read_csv(CSV_PATH, skiprows=1)
Att = '% of Attendance'

while True:
    display_choice()
    choice = int(input('Enter your choice: '))
    if choice == 0:
        break
    elif choice == 1:
        print("The student records are: ", *df.values, sep='\n')
    elif choice == 2:
        Name = input('Enter name of specific student: ').upper()
        records = df.loc[df['Student Name'] == Name].values
        print(records if records else "This name doesn't doesnt exist. Please recheck his spelling")

    elif choice == 3:
        maxi_data, *_ = df[df[Att] == max(df[Att])].values
        print(f'\nStudents having maximum % of Attendance: ')
        print(*maxi_data)

    elif choice == 4:
        mini_data, *_ = df[df[Att] == min(df[Att])].values
        print(f'\nStudent(s) having minimum % of Attendance: ')
        print(*mini_data)

    elif choice == 5:
        print(f'\nStudents having ({Att} <= 50%):')
        for person in df[df[Att] <= 50].values:
            print(*person)

    elif choice == 6:
        print(f'\nStudents in danger zone ({Att} <= 20%):')
        for person in df[df[Att] <= 20].values:
            print(*person)
    elif choice == 7:
        data = df[Att]
        print(*(
            ''
            f'Minimum {Att} is {data.min()}',
            f'Maximum {Att} is {data.max()}',
            f'Mean {Att} is {statistics.mean(data):.2f}',
            f'Median {Att} is {statistics.median(data):.2f}',
            f'Mode {Att} is {statistics.mode(data)}',
            f'Variance of {Att} is {statistics.variance(data):.2f}',
            f'Standard Deviation of {Att} is {statistics.stdev(data):.2f}',
        ), sep='\n')
    elif choice == 8:
        scatter_plot()
    elif choice == 9:
        bar_plot()
    elif choice == 10:
        pie_plot()
    elif choice == 11:
        line_plot()

    else:
        print("Invalid Choice. Try Again")
    if input('Continue? (y/n)').lower() != 'y':
        break

print("Thank you for using me")
