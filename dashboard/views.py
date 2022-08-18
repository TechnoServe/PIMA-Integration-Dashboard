import folium
import datetime
from django.http import Http404
from .constant_vars import regions
from django.shortcuts import render
from django.core.cache import cache
from folium.plugins import MarkerCluster
from PIMA_Dashboard.settings import BASE_DIR, env
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from dashboard.models import TrainingSession, DemoPlot, TrainingObservation, FarmVisit
from .utils import (
    add_basemap_layers,
    add_training_observations,
    add_training_sessions,
    add_demo_plots,
    add_required_objects,
    add_farm_visits
)


### INITIAL LOCATION SET-UP ##########
START_LOCATION = [-0.9019047458079028, 1.093501788502551]
####################################





@xframe_options_exempt
@login_required
def index(request):

    #MAP SETUP
    map = folium.Map(START_LOCATION, tiles=None, zoom_start=3)
    add_basemap_layers(map)      

    #FEATIRE-GROUPS SETUP
    featureGroup_training_observation = folium.FeatureGroup(name="TrainingObservations")
    featureGroup_training_sessions = folium.FeatureGroup(name="Training Sessions")
    featureGroup_demo_plots = folium.FeatureGroup(name="Demo Plots")
    featureGroup_farm_visits = folium.FeatureGroup(name="Farm Visits")

    #CLUSTER SETUP
    cluster_training_observations = MarkerCluster()
    cluster_training_sessions = MarkerCluster()
    cluster_demo_plots = MarkerCluster()
    cluster_farm_visits = MarkerCluster()

    if request.method == 'GET':

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=90) #3 months ago.

        #QUERY DATA
        TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date])
        TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date])
        Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date])
        FarmVisits = FarmVisit.objects.filter(Date_Visited_c__range=[start_date, end_date])


        #ADD TrainingObservations on MAP
        add_training_observations(map, TrainingObservations, cluster_training_observations, featureGroup_training_observation)

        #ADD Training Sessions on MAP 
        add_training_sessions(map, TrainingSessions, cluster_training_sessions, featureGroup_training_sessions)

        #ADD DemoPlot on MAP
        add_demo_plots(map, Demoplots, cluster_demo_plots, featureGroup_demo_plots)

        #ADD FarmVisit to MAP
        add_farm_visits(map, FarmVisits, cluster_farm_visits, featureGroup_farm_visits)
        

        #ADD: legend && Layer controller
        add_required_objects(map)

        programs = list(cache.get('Programs').values())

        context = {
            'map': map._repr_html_(),
            'programs': programs,
            'regions': regions
        }
        return render(request, 'dashboard/index.html', context)


    if request.method == 'POST':

        #GETTING DATES
        end_date_ = request.POST.get('end-date')
        start_date_ = request.POST.get('start-date')

        if(len(end_date_) == 0): end_date = datetime.date.today()
        else: end_date = datetime.date.fromisoformat(end_date_)

        if (len(start_date_) == 0): start_date = end_date - datetime.timedelta(days=3650) # 10 years ago
        else: start_date = datetime.date.fromisoformat(start_date_)

        #GETTING: programs
        selected_programs = request.POST.getlist('programs')
        
        if (len(selected_programs) == 0):
            TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date])
            TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date])
            Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date])
            FarmVisits = FarmVisit.objects.filter(Date_Visited_c__range=[start_date, end_date])

        else:
            TrainingObservations = TrainingObservation.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            TrainingSessions = TrainingSession.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            Demoplots = DemoPlot.objects.filter(Date_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)
            FarmVisits = FarmVisit.objects.filter(Date_Visited_c__range=[start_date, end_date]).filter(Program_c__in=selected_programs)


        #TrainingObservations
        add_training_observations(map, TrainingObservations, cluster_training_observations, featureGroup_training_observation)

        #Training Sessions
        add_training_sessions(map, TrainingSessions, cluster_training_sessions, featureGroup_training_sessions)

        #DemoPlot
        add_demo_plots(map, Demoplots, cluster_demo_plots, featureGroup_demo_plots)

        #ADD FarmVisit to MAP
        add_farm_visits(map, FarmVisits, cluster_farm_visits, featureGroup_farm_visits)

        add_required_objects(map)  

        programs = list(cache.get('Programs').values())
        
        context = {
            'map': map._repr_html_(),
            'programs': programs,
            'regions': regions,
            'selected_programs':selected_programs,
            'start_date': start_date_,
            'end_date': end_date_
        }   
        return render(request, 'dashboard/index.html', context)


@xframe_options_exempt
def project_details(request, slug=None):
    
    #MAP SETUP
    map = folium.Map(START_LOCATION, tiles=None, zoom_start=3)
    add_basemap_layers(map)      

    #FEATIRE-GROUPS SETUP
    featureGroup_training_observation = folium.FeatureGroup(name="TrainingObservations")
    featureGroup_training_sessions = folium.FeatureGroup(name="Training Sessions")
    featureGroup_demo_plots = folium.FeatureGroup(name="Demo Plots")
    #featureGroup_farm_visits = folium.FeatureGroup(name="Farm Visits")

    #CLUSTER SETUP
    cluster_training_observations = MarkerCluster()
    cluster_training_sessions = MarkerCluster()
    cluster_demo_plots = MarkerCluster()
    #cluster_farm_visits = MarkerCluster()

    if slug is not None:
        
        if request.method == 'POST':
            #GETTING DATES
            end_date_ = request.POST.get('end-date')
            start_date_ = request.POST.get('start-date')

            if(len(end_date_) == 0): end_date = datetime.date.today()
            else: end_date = datetime.date.fromisoformat(end_date_)

            if (len(start_date_) == 0): start_date = end_date - datetime.timedelta(days=3650) # 10 years ago
            else: start_date = datetime.date.fromisoformat(start_date_)
        
            query_training_observations =  TrainingObservation.objects.filter(Project_Name_c_slug__iexact=slug).filter(Date_c__range=[start_date, end_date])
            query_training_sessions = TrainingSession.objects.filter(Project_Name_c_slug__iexact=slug).filter(Date_c__range=[start_date, end_date])
            query_demo_plots = DemoPlot.objects.filter(Project_Name_c_slug__iexact=slug).filter(Date_c__range=[start_date, end_date])
            

            #TrainingObservations
            add_training_observations(map, query_training_observations, cluster_training_observations, featureGroup_training_observation)

            #Training Sessions
            add_training_sessions(map, query_training_sessions, cluster_training_sessions, featureGroup_training_sessions)

            #DemoPlot
            add_demo_plots(map, query_demo_plots, cluster_demo_plots, featureGroup_demo_plots)

            add_required_objects(map)  

            context = {'map': map._repr_html_(), 'slug':slug, 'start_date': start_date_, 'end_date': end_date_}
            return render(request, 'dashboard/project.html', context)

        
        if request.method == 'GET':

            query_training_observations =  TrainingObservation.objects.filter(Project_Name_c_slug__iexact=slug)
            query_training_sessions = TrainingSession.objects.filter(Project_Name_c_slug__iexact=slug)
            query_demo_plots = DemoPlot.objects.filter(Project_Name_c_slug__iexact=slug)
            
            #TrainingObservations
            add_training_observations(map, query_training_observations, cluster_training_observations, featureGroup_training_observation)

            #Training Sessions
            add_training_sessions(map, query_training_sessions, cluster_training_sessions, featureGroup_training_sessions)

            #DemoPlot
            add_demo_plots(map, query_demo_plots, cluster_demo_plots, featureGroup_demo_plots)

            add_required_objects(map)  

            context = {'map': map._repr_html_(), 'slug':slug}
            return render(request, 'dashboard/project.html', context)

    else:
        raise Http404


@login_required
def project_list(request):

    projects =  cache.get('Projects')
    projects_ = dict()

    for proj in projects: projects_[proj] = slugify(proj)
    
    context = {'projects': projects_}
    return render(request, 'dashboard/project_list.html', context)
