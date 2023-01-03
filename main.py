import requests #module for url
from bs4 import BeautifulSoup # module for parsing
import time #  module for finish program
import smtplib # module for email

# main class
class Currency:
	# links
	DOLLAR_SOM = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%BE%D0%BC%D1%83&ei=qVe0Y-KFJJCNxc8PhLiX2Ac&ved=0ahUKEwii_v306Kv8AhWQRvEDHQTcBXsQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%BE%D0%BC%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIQCAAQgAQQsQMQgwEQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoOCC4QgAQQsQMQxwEQ0QM6DgguEIAEELEDEIMBENQCOgsIABCABBCxAxCDAToICAAQgAQQsQM6CwguEIAEELEDEIMBOggIABAKEAEQQzoRCC4QgAQQsQMQgwEQxwEQ0QM6BQguEIAEOg8IABAKEAEQQxAqEEYQggI6CQgAEIAEEAoQAToECAAQQzoICAAQsQMQgwE6CggAELEDEIMBEEM6CAguELEDEIMBOg8IABCxAxCDARBDEEYQggI6BwgAELEDEEM6DQgAEIAEELEDEIMBEAo6BwgAEIAEEAo6CAgAEIAEEMkDSgQIQRgASgQIRhgAUM8GWJ6AvgFgmoK-AWgFcAF4AIABzwGIAbsVkgEGMC4xNS4xmAEAoAEBsAEAwAEB&sclient=gws-wiz-serp'
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

	current_converted_price = 0
	difference = 5 # after this difference message will be send to email

	def __init__(self):
		#setting up currency
		self.current_converted_price = float(self.get_currency_price().replace(",", "."))

	# metode to get currency
	def get_currency_price(self):
		# parsing all of site
		full_page = requests.get(self.DOLLAR_SOM, headers=self.headers)
		soup = BeautifulSoup(full_page.content, 'html.parser')

		# get what we need
		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		return convert[0].text

	# checking the changing of currency
	def check_currency(self):
		currency = float(self.get_currency_price().replace(",", "."))
		if currency >= self.current_converted_price + self.difference:
			print("The currency has grown a lot, maybe it's time to do something?")
			self.send_mail()
		elif currency <= self.current_converted_price - self.difference:
			print("The currency has dropped a lot, maybe it's time to do something?")
			self.send_mail()

		print("Now currency is : 1 $ = " + str(currency))
		time.sleep(3) 
		self.check_currency()

	# send message to email with SMTP
	def send_mail(self):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('your email', 'password')

		subject = 'Currency mail'
		body = 'Currency has been changed!' 
		message = f'Subject: {subject}\n{body}'

		server.sendmail(
			'from whom',
			'to who',
			message
		)
		server.quit()

# create object and call a method
currency = Currency()
currency.check_currency()
