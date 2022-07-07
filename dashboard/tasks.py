import requests
from celery import shared_task
from django.core.cache import cache
from PIMA_Dashboard.settings import env
from simple_salesforce import Salesforce

SALESFORCE_INSTANCE = env('SALESFORCE_INSTANCE')

def getToken():
    PARAMS = {
        'grant_type' : 'password',
        'client_id' : env('SALESFORCE_CLIENT_ID'),
        'client_secret' : env('SALESFORCE_SECRET'),
        'username' : env('SALESFORCE_USERNAME'),
        'password' : env('SALESFORCE_PASSWORD')
    }
    result =  requests.post(f'https://{SALESFORCE_INSTANCE}/services/oauth2/token', params=PARAMS)
    return result.json().get('access_token')


@shared_task(bind=True)
def getObservations(self):
    
    Observations = list()
    holder = dict()

    TOKEN = getToken()
    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)

    Obs_result = sf.query_all(
        "SELECT Id,Date__c,Project_Name__c,Observation_Location__Latitude__s,Observation_Location__Longitude__s,Trainer__c FROM Observation__c WHERE Date__c >= 2022-06-01"
    )
    
    Obs_records =  Obs_result.get('records')

    for row in Obs_records:
        holder['Id'] = row.get('Id')
        holder['Project_Name__c'] = row.get('Project_Name__c')
        holder['Trainer__c'] = row.get('Trainer__c') #trainer = sf.Contact.get('0031o00001Zxz7pAAB')
        holder['Observation_Location__Latitude__s'] =  row.get('Observation_Location__Latitude__s')
        holder['Observation_Location__Longitude__s'] = row.get('Observation_Location__Longitude__s')
        holder['Date__c'] = row.get('Date__c')
        Observations.append(holder)
        holder = {}
    
    #Write to caches
    cache.set('Observations', Observations)
    return "Done"



@shared_task(bind=True)
def getPrograms(self):

    TOKEN = getToken()
    
    Programs = list()
    holder = dict()
    
    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)
    programs = sf.query_all("SELECT Id,Name FROM Program__c")
    
    program_records =  programs.get('records')
    

    for row in program_records:
        holder['Id'] = row.get('Id')
        holder['Name'] = row.get('Name')
        Programs.append(holder)
        holder = {}

    cache.set('Programs', Programs)
    return "Done"
