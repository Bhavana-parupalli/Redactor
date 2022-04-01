import pytest
from project1 import project1

def test_names():
    doc = '''X-From: Kevin Whitehurst
             X-To: Rod Nelson, Tanya Rohauer
             John will assist you with any questions you may have'''
    (doc,names_redacted)=project1.names(doc)
    assert len(names_redacted)==4

def test_dates():
    doc='''Date: Wed, 17 Jan 2001 02:33:00 -0800 (PST)
           John will assist you with any questions you may have and if you are interested in ClickAtHome program you can contact him :
           1/16/2001  8:00:00 AM-5:00:00 PM'''
    (doc,dates_redacted)=project1.dates(doc)
    assert len(dates_redacted)==2

def test_phonenumbers():
    doc='''John will assist you with any questions you may have and if you are interested in ClickAtHome program you can contact him :
           (713) 853 7257'''
    (doc,phonenumbers_redacted)=project1.phone_numbers(doc)
    assert len(phonenumbers_redacted)==1

def test_gender():
    doc='''John will assist you with any questions you may have and if you are interested in ClickAtHome program you can contact him :'''
    (doc,genders_redacted)=project1.gender(doc)
    assert len(genders_redacted)==1

def test_address():
    doc='''1200 New Hampshire Avenue, NW
           Washington DC  
           (713) 853 7257'''
    (doc,address_redacted)=project1.address(doc)
    assert len(address_redacted)==3

def test_concept():
    doc='''We are excited to extend an invitation to you to participate in Pilot 3 of 
    Enron's new ClickAtHome program which is all about online network.  

    The ClickAtHome program is Enron's innovative solution to provide eligible 
    employees with a high-end computer and high-speed Internet connection.  If 
    you are interested in participating in the ClickAtHome pilot program, please 
    read about  "How to get started in Pilot 3" by clicking the link below.

    PC Ordering for Pilot 3 is now available with select Internet Service 
    Provider (ISP) ordering available by the end of the month. To get more 
    information about the web or place your order, visit http://clickathomepilot.enron.com.'''
    word='web'
    (doc,sentences_redacted)=project1.concept(doc,word)
    assert len(sentences_redacted)==4



