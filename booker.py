from selenium import webdriver
from datetime import datetime  
from datetime import timedelta  
import time
import schedule
import calendar
import os
import logging
import traceback

logging.basicConfig(filename="../"+datetime.now().strftime('booker_%d_%m_%Y.log'),level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s')
blacklistDates = [["Fri","Sat","Sun"],["Sat","Sun"]]
DEBUG_PREFIX = " [doBooking] "
def isExistBooking(index,driver):
	global blacklistDates
	targetDate = datetime.now() + timedelta(days=5)  
	logging.info(DEBUG_PREFIX+("Target date : "+ str(targetDate)))
	targetDay = calendar.day_name[targetDate.weekday()][:3]
	logging.info(DEBUG_PREFIX+("Target Day : "+ str(targetDay)))
	if(targetDay in blacklistDates[index]):
		return True
	time.sleep(10)
	bookings = driver.find_element_by_id("Bookings")
	
	apptTable = bookings.find_element_by_class_name("table")
	rows  = apptTable.find_elements_by_tag_name("tr")
	for index in range(len(rows)):
		if(index  == 0):
			continue
		row  = rows[index]
		day  = row.find_elements_by_tag_name("td")[0]
		if(day.text[:3] == targetDay):
			return True	
	return False		


def logout(driver):
	menu = driver.find_elements_by_class_name("dropdown-toggle")[1]
	menu.click()
	submenu = driver.find_elements_by_class_name("dropdown-menu")[1]
	logout = submenu.find_elements_by_tag_name("li")[17]
	logout.click()

def doBooking():
	logging.info(DEBUG_PREFIX+"Start")
	users = ["boyala@ualberta.ca","rukhmani@ualberta.ca"]
	pwds = ["Hitachi123!","Jaishriram24"]
	for i in range(len(users)):
		try:
			logging.info(DEBUG_PREFIX+"Start for user "+str(users[i]))
			logging.info(DEBUG_PREFIX+"Ctreating web driver")
			driver = webdriver.Chrome('/home/bijinbenny/Project/Selenium/book-myGym-UofA/chromedriver')

			driver.get("https://www.activityreg.ualberta.ca/UOFA/public/Logon/Logon")
			logging.info(DEBUG_PREFIX+"Sending username")
			username = driver.find_element_by_id("EmailAddress")
			username.clear()
			username.send_keys(users[i])
			logging.info(DEBUG_PREFIX+"Sending password")
			password = driver.find_element_by_name("Password")
			password.clear()
			password.send_keys(pwds[i])

			submit  = driver.find_element_by_class_name("btn-primary")
			submit.click()


			if(isExistBooking(i,driver)):
				logging.info(DEBUG_PREFIX+"Booking exists or date not required. Logging out..")
				logout(driver)
				driver.close()
				logging.info(DEBUG_PREFIX+"Logout successful")
				continue
			logging.info(DEBUG_PREFIX+"Booking does not exist. Continue booking..")	
			driver.find_element_by_link_text("Browse our Programs").click()
			driver.find_elements_by_class_name("media-heading")[0].click()
			driver.find_elements_by_class_name("media-heading")[2].click()
			driver.find_element_by_tag_name('h4').click()
			day = driver.find_elements_by_class_name("btn-default")[9]
			logging.info(DEBUG_PREFIX+"Booking for "+day.text)	
			day.click()	
			table  = driver.find_elements_by_class_name("table")[0]
			rows = table.find_elements_by_tag_name("tr")
			for index in range(len(rows)):
				if(index == 0):
					continue
				row = rows[index]	
				bookTime = row.find_elements_by_tag_name("td")[0]	
				logging.info(DEBUG_PREFIX+bookTime.text)
				if(bookTime.text == "6:00 PM"):
					logging.info(DEBUG_PREFIX+"Time 6 PM found")
					row.find_elements_by_tag_name("td")[6].click()
					time.sleep(10)
					driver.find_element_by_css_selector('a.btn-primary').click()
					logging.info(DEBUG_PREFIX+"Booking done")
		except Exception as e: 
			logging.exception("message")
		logging.info(DEBUG_PREFIX+"End for user "+str(users[i]))					
	logging.info(DEBUG_PREFIX+"End")
		

if(os.fork()>0):
	exit()
else:
	
	#Test code
	#doBooking()
	
	 logging.info("Start thread....")
	 schedule.every(1).hour.do(doBooking) 
	 logging.info("Schedule job registered")
	 while True: 
	 	schedule.run_pending() 
	 	time.sleep(1) 