import requests
import datetime
from celery import shared_task
from django.core.cache import cache
from PIMA_Dashboard.settings import env
from simple_salesforce import Salesforce
from dashboard.models import DemoPlot, TrainingObservation, TrainingSession, FarmVisit

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


###################################################################
@shared_task(bind=True)
def getProgramsAndProjects(self):
    #PROJECT_FORMAT: {'project_name':'program_name', ...}
    #PROGRAM_FORMAT: {'id':'program_name', ...}


    TOKEN = getToken()
    
    Projects = dict()
    Programs = dict()
    
    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)

    programs = sf.query_all("SELECT Id,Name FROM Program__c WHERE IsDeleted=false")
    projects = sf.query_all("SELECT Name,Program__c FROM Project__c WHERE IsDeleted=false")
    
    programs =  programs.get('records')
    projects =  projects.get('records')

    for program in programs:
        if('Coffee' not in program.get('Name')): continue
        Programs[program.get('Id')] = program.get('Name')
    
    for project in projects:
        try:
            Projects[project.get('Name')] = Programs[project.get('Program__c')]
        except:
            continue

        #Projects[project.get('Name')] = Programs.get(project.get('Program__c'))

    cache.set('Projects', Projects)
    cache.set('Programs', Programs)

    return "DONE"
##############################################################################



@shared_task(bind=True)
def getTrainingObservations(self):
    
    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    Obs = sf.query("SELECT Id,Date__c,Project_Name__c,Observation_Location__Latitude__s,Observation_Location__Longitude__s,Trainer__r.Name,Number_of_Participants__c FROM Observation__c WHERE IsDeleted=false AND RecordType.Name = 'Training' AND Observation_Location__Latitude__s != null AND Observation_Location__Longitude__s != null")
    
    records.extend(Obs.get('records'))

    if Obs.get('done')is False:
        DONE = False
        while not DONE:
            Obs = sf.query_more(Obs.get('nextRecordsUrl'), True)
            records.extend(Obs.get('records'))
            DONE = Obs.get('done')

    #Cache to REDIS
    cache.set('Observations', records)
    
    # Get the orject to help find the program
    Projects =  cache.get('Projects')

    #Add to SQLite
    TrainingObservation.objects.all().delete() #Delete all records before adding new

    for record in records:
        if(record.get('Observation_Location__Latitude__s') == None or record.get('Observation_Location__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date__c'))
        except:
            date_ = None

        TrainingObservation.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_c = date_,
            Project_Name_c =  record.get('Project_Name__c'),
            Program_c = Projects.get(record.get('Project_Name__c')),
            Observation_Location_Latitude_s = record.get('Observation_Location__Latitude__s'),
            Observation_Location_Longitude_s = record.get('Observation_Location__Longitude__s'),
            Trainer_c = record.get('Trainer__r').get('Name') if record.get('Trainer__r') is not None else 'null',
            Number_of_Participants_c = record.get('Number_of_Participants__c')
        )

    return "DONE"
##################################################################

@shared_task(bind=True)
def getTrainingSessions(self):
    
    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    TSs = sf.query("SELECT Id,Date__c,Project_Name__c,Location_GPS__Latitude__s,Location_GPS__Longitude__s, Number_in_Attendance__c,Module_Name__c,Trainer__r.Name,Training_Group__r.Name,Program__c FROM Training_Session__c WHERE IsDeleted=false AND Location_GPS__Latitude__s != null AND Location_GPS__Longitude__s != null")
    
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
    TrainingSession.objects.all().delete() #Delete all records before adding new
    
    for record in records:
        if(record.get('Location_GPS__Latitude__s') == None or record.get('Location_GPS__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date__c'))
        except:
            date_ = None

        TrainingSession.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_c = date_,
            Location_GPS_Latitude_s = record.get('Location_GPS__Latitude__s'),
            Location_GPS_Longitude_s = record.get('Location_GPS__Longitude__s'),
            Project_Name_c = record.get('Project_Name__c'),
            Trainer_c = record.get('Trainer__r').get('Name') if record.get('Trainer__r') is not None else 'null',
            Program_c = record.get('Program__c'),
            Training_Group_c = record.get('Training_Group__r').get('Name') if record.get('Training_Group__r') is not None else 'null',
            Module_Name_c = record.get('Module_Name__c'),
            Number_in_Attendance_c = record.get('Number_in_Attendance__c')
        )

    return "DONE"



@shared_task(bind=True)
def getDemoPlots(self):
    
    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    Demoplots = sf.query("SELECT Id,Date__c,Project_Name__c,Observation_Location__Latitude__s,Observation_Location__Longitude__s,Trainer__r.Name,Number_of_Participants__c FROM Observation__c WHERE IsDeleted=false AND RecordType.Name = 'Demo Plot' AND Observation_Location__Latitude__s != null AND Observation_Location__Longitude__s != null")
    
    records.extend(Demoplots.get('records'))

    if Demoplots.get('done')is False:
        DONE = False
        while not DONE:
            Demoplots = sf.query_more(Demoplots.get('nextRecordsUrl'), True)
            records.extend(Demoplots.get('records'))
            DONE = Demoplots.get('done')

    #Cache to REDIS
    cache.set('DemoPlots', records)
    
    # Get the projects to help find the program
    Projects =  cache.get('Projects')

    #Add to SQLite
    DemoPlot.objects.all().delete() #Delete all records before adding new

    for record in records:
        if(record.get('Observation_Location__Latitude__s') == None or record.get('Observation_Location__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date__c'))
        except:
            date_ = None

        DemoPlot.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_c = date_,
            Project_Name_c =  record.get('Project_Name__c'),
            Program_c = Projects.get(record.get('Project_Name__c')),
            Observation_Location_Latitude_s = record.get('Observation_Location__Latitude__s'),
            Observation_Location_Longitude_s = record.get('Observation_Location__Longitude__s'),
            Trainer_c = record.get('Trainer__r').get('Name') if record.get('Trainer__r') is not None else 'null',
            Number_of_Participants_c = record.get('Number_of_Participants__c')
        )

    return "DONE"

@shared_task(bind=True)
def getFarmVisits(self):
    #QUERY
    #SELECT Id,OwnerId,Date_Visited__c,Location_GPS__Latitude__s,Location_GPS__Longitude__s,Farmer_Trainer__r.Name,Training_Group__r.Name FROM Farm_Visit__c WHERE IsDeleted=false AND Location_GPS__Latitude__s != null AND Location_GPS__Longitude__s != null

    records = list()
    TOKEN = getToken()

    sf = Salesforce(instance_url=f'https://{SALESFORCE_INSTANCE}', session_id=TOKEN)    
    FarmVisits = sf.query("SELECT Id,Date_Visited__c,Location_GPS__Latitude__s,Location_GPS__Longitude__s,Farmer_Trainer__r.Name,Training_Group__r.Name FROM Farm_Visit__c WHERE IsDeleted=false AND Location_GPS__Latitude__s != null AND Location_GPS__Longitude__s != null")
    
    records.extend(FarmVisits.get('records'))

    if FarmVisits.get('done')is False:
        DONE = False
        while not DONE:
            FarmVisits = sf.query_more(FarmVisits.get('nextRecordsUrl'), True)
            records.extend(FarmVisits.get('records'))
            DONE = FarmVisits.get('done')

    #Cache to REDIS
    cache.set('FarmVisits', records)
    
    # Get the projects to help find the program
    #Projects =  cache.get('Projects')

    #Add to SQLite
    FarmVisit.objects.all().delete() #Delete all records before adding new

    for record in records:
        if(record.get('Location_GPS__Latitude__s') == None or record.get('Location_GPS__Longitude__s') == None): continue
        
        try:
            date_ = datetime.date.fromisoformat(record.get('Date_Visited__c'))
        except:
            date_ = None

        FarmVisit.objects.create(
            Salesforce_Id=record.get('Id'),
            Date_Visited_c = date_,
            #Project_Name_c =  record.get('Project_Name__c'),
            #Program_c = Projects.get(record.get('Project_Name__c')),
            Location_GPS_Latitude_s = record.get('Location_GPS__Latitude__s'),
            Location_GPS_Longitude_s = record.get('Location_GPS__Longitude__s'),
            Farmer_Trainer_c = record.get('Farmer_Trainer__r').get('Name') if record.get('Farmer_Trainer__r') is not None else 'null',
            Training_Group_c = record.get('Training_Group__r').get('Name') if record.get('Training_Group__r') is not None else 'null'
        )

    return "DONE"


##################################################################