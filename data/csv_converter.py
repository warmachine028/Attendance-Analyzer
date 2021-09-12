import csv

import camelot

IN_PATH = 'student_attendance.pdf'
OUT_PATH = f'{IN_PATH[:-3]}csv'


class Converter:
    def __init__(self, input_path, output_path):
        self.in_path = input_path
        self.out_path = output_path

    def table_to_csv(self, tables):
        with open(self.out_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for t, table in enumerate(tables):
                if t == 0:
                    table.df[2][1], table.df[3][1] = "Enrollment No.", "Registration No."
                writer.writerows(table.df.values)

    def convert(self):
        tables = camelot.read_pdf('student_attendance.pdf', pages='all', split_text=True, strip_text='\n')
        self.table_to_csv(tables)


if __name__ == '__main__':
    Converter(IN_PATH, OUT_PATH).convert()
