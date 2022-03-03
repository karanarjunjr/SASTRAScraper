from django.shortcuts import render, redirect
from .forms import Email
from .models import Recepient
from .models import ListItem
import requests
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

def sendEmail():
    URL = "https://www.sastra.edu/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="user6")
    elements = results.findAll("li")
    titles = [x.getText() for x in elements]
    links = [x.a['href'] for x in elements]

    dic1 = {titles[i] : links[i] for i in range(len(titles))}
    dic2 = {x.title : x.link for x in ListItem.objects.all()}
    mailDic = {}
    
    # Checking for new keys
    for key in dic1:
        if key not in dic2:
            mailDic[key] = dic1[key]
            dic2[key] = dic1[key]
            ListItem.objects.create(title=key, link=dic1[key])

    # Checking for removed keys
    for key in dic2:
        if key not in dic1:
            del dic2[key]
            ListItem.objects.filter(title=key).delete()

    if not bool(mailDic):
        return

    # Sending email
    server = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
    server.starttls()
    server.ehlo()
    server.login("sastrascraper@gmail.com", 'thekick17')
    sent_from = "sastrascraper@gmail.com"
    to = [x.Email for x in Recepient.objects.all()]
    subject = 'SASTRA Announcement'
    body = ""

    for key in mailDic:
        body += key + "     https://www.sastra.edu" + mailDic[key] + "\n"

    email_text = EmailMessage()

    email_text['Subject'] = subject
    email_text['FROM'] = sent_from
    email_text['TO'] = to
    email_text.set_content(body)
    server.send_message(email_text)
    print ('Email sent!')
    server.quit()

def addRecipient(emailID):
    last = emailID[-13:] 
    if (last == "@sastra.ac.in" and not Recepient.objects.filter(Email=emailID).exists()):
        Recepient.objects.create(Email=emailID)
        return True
    return False

def delRecipient(emailID):
    last = emailID[-13:] 
    if (last == "@sastra.ac.in" and Recepient.objects.filter(Email=emailID).exists()):
        Recepient.objects.filter(Email=emailID).delete()
        return True
    return False


def submit(request):
    if request.method == 'POST':
        form = Email(request.POST)
        if form.is_valid():
            if 'add' in request.POST:
                if addRecipient(form.cleaned_data['Email']):
                    return render(request, 'main/success.html')
                else:
                    return render(request, 'main/failure.html')
            else:
                if delRecipient(form.cleaned_data['Email']):
                    return render(request, 'main/success.html')
                else:
                    return render(request, 'main/failure.html')
    else:
        form = Email()
    return render(request, 'main/index.html', {'form': form})