import JsonParser as jp
import smtplib, ssl

sender_email = "toilets4london@gmail.com"


def send_message(name, opening_hours, disabled, location, receiver_email):
    message = """Subject: Your toilet is listed on OpenStreetMap 

    Hi %s!
    
    My name is Nina and I am a student at Imperial College London. I am planning to release an app that allows Londoners to locate, access and rate public and private toilets in London. You may be aware that lack of public toilets is a big issue in our city, and those public toilets that are available are often unhygienic and not well looked after. The data used in this app will in part come from OpenStreetMap (https://www.openstreetmap.org/). I have come across your business as one of a few businesses in London already listed as having a toilet. Unlike similar apps, Toilets4London prides itself on the accuracy of its data. Therefore, it would be super if you could reply to confirm the details of your toilet.
    
    This is the data we currently have:
    Location: %s
    Opening Hours: %s
    Disabled Accessibility: %s
    
    In addition to confirming these details, I was wondering whether you would consider opening your toilet up for public use through the app. If you sign up to the Toilets4London community toilet scheme, you will get free publicity as locals will see your business is taking part in this initiative to make London more open and accessible.
    
    Let me know in your reply if you would like any more information about Toilets4London or would like to sign up to the scheme.
    
    Thank you for your help and hope to hear from you soon,
    Nina,
    Toilets4London""" % (name, location, opening_hours, disabled)

    port = 465  # For SSL
    password = input("Type your password and press enter to send email: ")
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def safe_print(a_dict, key):
    try:
        print(a_dict[key])
        return a_dict[key]
    except KeyError:
        return None


with open("Data/emails.txt", 'r') as emails:
    all_emails_sent = emails.read()

with open("Data/emails.txt", 'a+') as emails:
    data = jp.load_all_json("Data/mixed_data.json")
    for e in data['elements']:
        tags = e['tags']
        email = safe_print(tags, key='email')
        if email:
            name = safe_print(tags, key='name')
            disabled = safe_print(tags, key='toilets:wheelchair')
            opening = safe_print(tags, key='opening_hours')
            postcode = safe_print(tags, key='addr:postcode')
            number = safe_print(tags, key='addr:housenumber')
            street = safe_print(tags, key='addr:street')
            if not name:
                name = ""
            if not disabled:
                disabled = "Not specified"
            if not opening:
                opening = "Not specified"

            if not (street or postcode or number):
                address = "Not specified"
            else:
                if not postcode:
                    postcode = ""
                if not number:
                    number = ""
                if not street:
                    street = ""
                address = number+" "+street+" "+postcode

            if email not in all_emails_sent:
                send_message(name=name, disabled=disabled, opening_hours=opening, location=address, receiver_email=email)
                emails.write(email+"\n")





