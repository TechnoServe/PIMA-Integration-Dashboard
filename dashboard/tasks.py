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
    
    Observation_Ids = list()
    Observations = list()
    holder = dict()

    TOKEN = getToken()
    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)
    Obs_result = sf.query_all("SELECT Id FROM Observation__c WHERE Date__c >= 2022-06-01")
    Obs_records =  Obs_result.get('records')

    for row in Obs_records:
        Observation_Ids.append(row.get('Id'))
    
    for id_ in Observation_Ids:

        current_obs = sf.Observation__c.get(id_)
        holder['Id'] = id_
        holder['Project_Name__c'] = current_obs.get('Project_Name__c')
        holder['Trainer__c'] = current_obs['Trainer__c'] #trainer = sf.Contact.get('0031o00001Zxz7pAAB')
        holder['Observation_Location__Latitude__s'] =  current_obs.get('Observation_Location__Latitude__s')
        holder['Observation_Location__Longitude__s'] = current_obs.get('Observation_Location__Longitude__s')
        holder['Date__c'] = current_obs.get('Date__c')
        Observations.append(holder)
        holder = {}
    
    #Write to caches
    cache.set('Observations', Observations)
    return "Done"
