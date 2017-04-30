from django.test import TestCase

# Create your tests here.

from utilities.templatetags.datefilters import format_date

class DateFormatTestCase(TestCase):
	def test_standard_date(self):
		result = format_date("1895-10-12")
		self.assertEqual(result, "12 Oct 1895")
	def test_date_already_formatted(self):
		result = format_date("15 Mar 1752")
		self.assertEqual(result, "15 Mar 1752")
	def test_zero_day(self):
		result= format_date("1564-06-00")
		self.assertEqual(result, "Jun 1564")
	def test_zero_month(self):
		result= format_date("1564-00-00")
		self.assertEqual(result, "1564")
	def test_zero_month_not_day(self):
		result= format_date("1564-00-12")
		self.assertEqual(result, "1564")
	def test_about_before_and_after(self):
		result= format_date("?1564-02-12")
		self.assertEqual(result, "ca. 12 Feb 1564")
		result= format_date("1564?")
		self.assertEqual(result, "ca. 1564")
