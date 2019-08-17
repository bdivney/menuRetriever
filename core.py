from botocore.vendored import requests
from datetime import datetime
import smtplib, ssl
import time

def lambda_handler(event, context):
    
    menu = menuNorth
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = ""  # Enter your address
    
    #People on distribution list
    directory = {
		"name" : "number"
    }
    

        
    
    receiver_emails = directory.values()  # Enter receiver address
    password = ''
    
    commonFoods = ['Grilled Cheese on White', 'Steamed Long Grain Rice', 'Steamed Brown Rice', 'Breaded Chicken Fillet', 'Malibu Vegan Gardenburger', 'Char-Grilled Chicken Breast']
    fuckingGross = ['Homestyle Vegan', 'Grill Non-entree', 'Pan-american', 'Salads', 'Soups', 'Pastaria', 'Pizzeria', 'Asian Stir Fry', 'Asian Parstock']
    alreadyPrinted = False
    r = requests.get(url=menu)
    data = r.json()
    today = datetime.today().strftime('%Y-%m-%d')
    
    
    def sendMessage(message, recipients):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipients, message)
    
    for entry in data:
        message = ""
        date = entry['EventStart'].split('T')[0]
        if(date == today and alreadyPrinted == False):
            for person, number in directory.items():
                m = "Good morning {}, today is {}. Here is the menu".format(person, date)
                sendMessage(m, number)
            time.sleep(5)
            alreadyPrinted = True
        if(date == today):
            message += '\n{}:\n'.format(entry['Meal'])
            print('\n{}:'.format(entry['Meal']))
            for course in entry['Courses']:
                if(course['Name'] not in fuckingGross):
                    message += '\n{}: \n'.format(course['Name'])
                    print('{}: '.format(course['Name']))
                    for menuItem in course['MenuItems']:
                        if(menuItem['Name'] not in commonFoods):
                            message += '->{}\n'.format(menuItem['Name'])
                            print('->{}'.format(menuItem['Name']))
            sendMessage(message, receiver_emails)
            time.sleep(5)
    
