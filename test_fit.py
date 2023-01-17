import unittest
from fit import Fit

class TestFit(unittest.TestCase):

	def test_size_not_within_range(self):

		with self.assertRaises(ValueError) as err:
			Fit(size=2, hole_toler='', shaft_toler='')

		self.assertEqual(type(err.exception), ValueError)
		self.assertEqual(
            err.exception.args[0], "Size value NOT within 3-400 range!"
        )

		with self.assertRaises(ValueError):
			Fit(size=401, hole_toler='M7', shaft_toler='e6')

	def test_empty_tolerance_grades(self):

		with self.assertRaises(ValueError) as err:
			Fit(size=3, hole_toler='', shaft_toler='')

		self.assertEqual(type(err.exception), ValueError)
		self.assertEqual(
            err.exception.args[0], "EMPTY input field(s)!"
        )

		with self.assertRaises(ValueError):
			Fit(size=3, hole_toler='E12', shaft_toler='')

	def test_tolerance_grade_not_in_database(self):

		with self.assertRaises(LookupError):
			Fit(size=3, hole_toler='E14', shaft_toler='h6')

		with self.assertRaises(LookupError):
			Fit(size=3, hole_toler='E12', shaft_toler='h13')

	def test_get_deviations(self):
		ES, EI, es, ei = Fit.get_deviations(size=50, hole_toler='M7', shaft_toler='e6')

		self.assertEqual(ES, 0)
		self.assertEqual(EI, -25)
		self.assertEqual(es, -50)
		self.assertEqual(ei, -66)

	def test_get_deviations_float(self):
		ES, EI, es, ei = Fit.get_deviations(size=50, hole_toler='M7', shaft_toler='js5')

		self.assertEqual(es, 5.5)
		self.assertEqual(ei, -5.5)

	def test_clearance_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='e6')

		self.assertEqual(fit.fit_type, 'Clearance')
		self.assertEqual(fit.c_max, 66)
		self.assertEqual(fit.c_min, 25)
		self.assertEqual(fit.c_avg, 45.5)

		self.assertEqual(fit.max_hole_size, 50.0)
		self.assertEqual(fit.min_hole_size, 49.975)
		self.assertEqual(fit.max_shaft_size, 49.95)
		self.assertEqual(fit.min_shaft_size, 49.934)

	def test_second_clearance_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='f5')

		self.assertEqual(fit.fit_type, 'Clearance')
		self.assertEqual(fit.c_max, 36)
		self.assertEqual(fit.c_min, 0)
		self.assertEqual(fit.c_avg, 18)

		self.assertEqual(fit.max_hole_size, 50.0)
		self.assertEqual(fit.min_hole_size, 49.975)
		self.assertEqual(fit.max_shaft_size, 49.975)
		self.assertEqual(fit.min_shaft_size, 49.964)

	def test_interference_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='k5')

		self.assertEqual(fit.fit_type, 'Interference')
		self.assertEqual(fit.i_max, 38)
		self.assertEqual(fit.i_min, 2)
		self.assertEqual(fit.i_avg, 20) 

		self.assertEqual(fit.max_shaft_size, 50.013)
		self.assertEqual(fit.min_shaft_size, 50.002)

	def test_transition_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='g5')

		self.assertEqual(fit.fit_type, 'Transition')
		self.assertEqual(fit.c_max, 20)
		self.assertEqual(fit.i_max, 16)
		self.assertEqual(fit.transition, 4)

		self.assertEqual(fit.max_shaft_size, 49.991)
		self.assertEqual(fit.min_shaft_size, 49.98)

	def test_second_transition_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='g7')

		self.assertEqual(fit.fit_type, 'Transition')
		self.assertEqual(fit.c_max, 34)
		self.assertEqual(fit.i_max, 16)
		self.assertEqual(fit.transition, 18)

		self.assertEqual(fit.max_shaft_size, 49.991)
		self.assertEqual(fit.min_shaft_size, 49.966)

	def test_third_transition_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='h5')

		self.assertEqual(fit.fit_type, 'Transition')
		self.assertEqual(fit.c_max, 11)
		self.assertEqual(fit.i_max, 25)
		self.assertEqual(fit.transition, -14)

		self.assertEqual(fit.max_shaft_size, 50)
		self.assertEqual(fit.min_shaft_size, 49.989)

	def test_fourth_transition_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='h7')

		self.assertEqual(fit.fit_type, 'Transition')
		self.assertEqual(fit.c_max, 25)
		self.assertEqual(fit.i_max, 25)
		self.assertEqual(fit.transition, 0)

		self.assertEqual(fit.max_shaft_size, 50)
		self.assertEqual(fit.min_shaft_size, 49.975)

	def test_fifth_transition_fit(self):
		fit = Fit(size=50, hole_toler='M7', shaft_toler='js5')

		self.assertEqual(fit.fit_type, 'Transition')
		self.assertEqual(fit.c_max, 5.5)
		self.assertEqual(fit.i_max, 30.5)
		self.assertEqual(fit.transition, -25)

		self.assertEqual(fit.max_shaft_size, 50.0055)
		self.assertEqual(fit.min_shaft_size, 49.9945)

if __name__ == '__main__':
	unittest.main()
