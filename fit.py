import csv


class Fit:

    HOLES_CSV_PATH = 'tolerances/iso_tolerances_holes.csv'
    SHAFTS_CSV_PATH = 'tolerances/iso_tolerances_shafts.csv'

    def __init__(self, size: int, hole_toler: str, shaft_toler: str):

        # Input data validation
        if not 3 <= size <= 400:
            raise ValueError(f'Size value NOT within 3-400 range!')

        elif not all([hole_toler, shaft_toler]):
            raise ValueError('EMPTY input field(s)!')

        elif hole_toler not in Fit.get_hole_toler_lst():
            raise LookupError(f'"{hole_toler}" was NOT FOUND in our database!')

        elif shaft_toler not in Fit.get_shaft_toler_lst():
            raise LookupError(f'"{shaft_toler}" was NOT FOUND in our database!')

        self.size = size
        self.hole_toler = hole_toler
        self.shaft_toler = shaft_toler

        for attr in ('c_max', 'c_min', 'c_avg', 'i_max', 'i_min', 'i_avg', 'transition'):
            setattr(self, attr, None)

        self.ES, self.EI, self.es, self.ei = Fit.get_deviations(size, hole_toler, shaft_toler)

        self.fit_designation = f'⌀{size} {hole_toler}/{shaft_toler}'

        self.max_hole_size = size + (self.ES / 1000)
        self.min_hole_size = size + (self.EI / 1000)
        self.max_shaft_size = size + (self.es / 1000)
        self.min_shaft_size = size + (self.ei / 1000)

        if self.EI >= self.es:
            self.fit_type = 'Clearance'
            self.c_max = self.ES - self.ei
            self.c_min = self.EI - self.es
            self.c_avg = (self.c_max + self.c_min) / 2

        elif self.ei >= self.ES:
            self.fit_type = 'Interference'
            self.i_max = self.es - self.EI
            self.i_min = self.ei - self.ES
            self.i_avg = (self.i_max + self.i_min) / 2

        else:
            self.fit_type = 'Transition'
            self.c_max = self.ES - self.ei
            self.i_max = self.es - self.EI
            self.transition = self.c_max - self.i_max

    @classmethod
    def get_hole_toler_lst(cls):
        """
        A class method to return a list
        of all hole tolerance grades
        which we have in our CSV
        """

        hole_toler_lst = list()

        with open(cls.HOLES_CSV_PATH, 'r') as hole_csv:
            csv_reader = csv.DictReader(hole_csv, delimiter='\t')
            for line in csv_reader:
                if (t := line['tolerance_gr']) not in hole_toler_lst:
                    hole_toler_lst.append(t)

        return hole_toler_lst

    @classmethod
    def get_shaft_toler_lst(cls):
        """
        A class method to return a list
        of all shaft tolerance grades
        which we have in our CSV
        """

        shaft_toler_lst = list()

        with open(cls.SHAFTS_CSV_PATH, 'r') as shaft_csv:
            csv_reader = csv.DictReader(shaft_csv, delimiter='\t')
            for line in csv_reader:
                if (t := line['tolerance_gr']) not in shaft_toler_lst:
                    shaft_toler_lst.append(t)

        return shaft_toler_lst

    @classmethod
    def get_deviations(cls, size, hole_toler, shaft_toler) -> tuple:
        """
        Return upper and lower deviations
        for both hole and shaft
        """
        deviations = {
            'ES': None,
            'EI': None,
            'es': None,
            'ei': None
        }

        with open(cls.HOLES_CSV_PATH, 'r') as holes_csv:
            csv_reader = csv.DictReader(holes_csv, delimiter='\t')

            for line in csv_reader:
                size_range = tuple(map(int, line['size'].split('-')))
                if size_range[0] < size <= size_range[1]:
                    if line['tolerance_gr'] == hole_toler:
                        deviations['ES'] = float(line['ES'])
                        deviations['EI'] = float(line['EI'])

        with open(cls.SHAFTS_CSV_PATH, 'r') as shafts_csv:
            csv_reader = csv.DictReader(shafts_csv, delimiter='\t')

            for line in csv_reader:
                size_range = tuple(map(int, line['size'].split('-')))
                if size_range[0] < size <= size_range[1]:
                    if line['tolerance_gr'] == shaft_toler:
                        deviations['es'] = float(line['es'])
                        deviations['ei'] = float(line['ei'])

        # Check if not found
        if deviations['ES'] is None:
            raise LookupError(f'{self.hole_toler} grade NOT applicable for size {self.size} mm!')
        elif deviations['es'] is None:
            raise LookupError(f'{self.shaft_toler} grade NOT applicable for size {self.size} mm!')

        # x.0 -> x
        for k, v in deviations.items():
            if int(v) == v:
                deviations[k] = int(v)

        return tuple(deviations.values())

    def show_info(self):
        """
        Print all attributes of the instance class
        """
        for k, v in self.__dict__.items():
            print(f'{k}: {v}')


def main():
    fit = Fit(size=50, hole_toler='M7', shaft_toler='k5')
    fit.show_info()


if __name__ == '__main__':
    main()
