import requests
import datetime
from celery import shared_task
from django.core.cache import cache
from PIMA_Dashboard.settings import env
from simple_salesforce import Salesforce
from dashboard.models import Observation_c, Training_Session_c

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
    
    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    Obs = sf.query("SELECT Id,Date__c,Project_Name__c,Observation_Location__Latitude__s,Observation_Location__Longitude__s,Trainer__c,Number_of_Participants__c FROM Observation__c WHERE IsDeleted=false")
    
    records.extend(Obs.get('records'))

    if Obs.get('done')is False:
        DONE = False
        while not DONE:
            Obs = sf.query_more(Obs.get('nextRecordsUrl'), True)
            records.extend(Obs.get('records'))
            DONE = Obs.get('done')

    #Cache to REDIS
    cache.set('Observations', records)

    #Add to SQLite
    Observation_c.objects.all().delete() #Delete all records before adding new
    
    for record in records:
        if(record.get('Observation_Location__Latitude__s') == None or record.get('Observation_Location__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date__c'))
        except:
            date_ = None

        Observation_c.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_c = date_,
            Project_Name_c =  record.get('Project_Name__c'),
            Observation_Location_Latitude_s = record.get('Observation_Location__Latitude__s'),
            Observation_Location_Longitude_s = record.get('Observation_Location__Longitude__s'),
            Trainer_c = record.get('Trainer__c'),
            Number_of_Participants_c = record.get('Number_of_Participants__c')
        )

    return "DONE"
##################################################################

@shared_task(bind=True)
def getTrainingSessions(self):
    
    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    TSs = sf.query("SELECT Id,Date__c,Project_Name__c,Location_GPS__Latitude__s,Location_GPS__Longitude__s, Number_in_Attendance__c,Module_Name__c,Trainer__c,Training_Group__c FROM Training_Session__c WHERE IsDeleted=false")
    
    records.extend(TSs.get('records'))

    if TSs.get('done')is False:
        DONE = False
        while not DONE:
            TSs = sf.query_more(TSs.get('nextRecordsUrl'), True)
            records.extend(TSs.get('records'))
            DONE = TSs.get('done')

    #Cache to REDIS
    cache.set('TrainingSessions', records)

    #Add to SQLite
    Training_Session_c.objects.all().delete() #Delete all records before adding new
    
    for record in records:
        if(record.get('Location_GPS__Latitude__s') == None or record.get('Location_GPS__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date__c'))
        except:
            date_ = None

        Training_Session_c.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_c = date_,
            Project_Name_c =  record.get('Project_Name__c'),
            Location_GPS_Latitude_s = record.get('Location_GPS__Latitude__s'),
            Location_GPS_Longitude_s = record.get('Location_GPS__Longitude__s'),
            Trainer_c = record.get('Trainer__c'),
            Training_Group_c = record.get('Training_Group__c'),
            Module_Name_c = record.get('Module_Name__c'),
            Number_in_Attendance_c = record.get('Number_in_Attendance__c')
        )

    return "DONE"



###################################################################
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
    return "DONE"
