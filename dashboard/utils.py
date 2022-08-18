import folium
from .legends import macro_legend
from .constant_vars import basemaps

def add_required_objects(map):
    map.add_child(folium.LayerControl())
    map.add_child(macro_legend)


def add_basemap_layers(map):
    '''
    Add basemap layer to the layer object.
    Selected basemaps: Google Satellite & Maps, ESRI Satellite.
    '''
    basemaps['Google Satellite'].add_to(map)
    basemaps['Google Maps'].add_to(map)
    basemaps['Esri Satellite'].add_to(map)

#TrainingObservations
def add_training_observations(map, training_observations ,cluster, feature_group):
    '''
    ADD Training Observations on the map
    '''
    for Observation in training_observations:
            cord = [Observation.Observation_Location_Latitude_s, Observation.Observation_Location_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue
            
            date_ = Observation.Date_c
            trainer_ = Observation.Trainer_c
            project_ = Observation.Project_Name_c
            participants_ = Observation.Number_of_Participants_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Project</i>:<b>{project_}</b></br><i>Participants</i>:<b>{participants_}</b><br><img src="https://www.technoserve.org/wp-content/uploads/2021/01/CajuLab-photo-1-300x225.png"/>'
            folium.Marker(
                    location=cord,
                    tooltip="Training Observation",
                    popup = pop_info,
                    icon=folium.Icon(color="red"),
                    ).add_to(cluster)
    cluster.add_to(feature_group)
    feature_group.add_to(map)

#Training Sessions
def add_training_sessions(map, training_sessions ,cluster, feature_group):
    '''
    ADD Training Sessions on the map
    '''
    for trainingsession in training_sessions:
            cord = [trainingsession.Location_GPS_Latitude_s, trainingsession.Location_GPS_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue

            date_ = trainingsession.Date_c
            trainer_ = trainingsession.Trainer_c
            group_ = trainingsession.Training_Group_c
            module_ = trainingsession.Module_Name_c
            project_ = trainingsession.Project_Name_c
            attendance_ = trainingsession.Number_in_Attendance_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Module</i>:<b>{module_}</b><br><i>Attendance</i>:<b>{attendance_}</b><br><i>Group</i>:<b>{group_}</b><br><i>Project</i>:<b>{project_}</b><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHYRZU5OjdnP0OKZWKIFy1aCnnlqRaVmVre2t3k3BVkVhIXYKLJjFe5Ng1mOXgWfVex2Y&usqp=CAU"/>'
            folium.Marker(
                location=cord,
                tooltip="Training Session",
                popup = pop_info,
                icon= folium.Icon(color="blue"),
                ).add_to(cluster)
    cluster.add_to(feature_group)
    feature_group.add_to(map)

def add_demo_plot(map, demo_plots, cluster, feature_group):
    '''
    ADD Demo Plots on the map
    '''
    for demo_plot in demo_plots:
            cord = [demo_plot.Observation_Location_Latitude_s, demo_plot.Observation_Location_Longitude_s]
            if(cord[0] is None or cord[1] is None): continue
            
            date_ = demo_plot.Date_c
            trainer_ = demo_plot.Trainer_c
            project_ = demo_plot.Project_Name_c
            participants_ = demo_plot.Number_of_Participants_c
            pop_info = f'<i>Date</i>:<b>{date_}</b><br><i>Trainer</i>:<b>{trainer_}</b><br><i>Project</i>:<b>{project_}</b></br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVrI_jVThOXGGjISB_9vrPQsGm3V8R_k8hj33_WXDqo2jVa8irSGx0Tpj0XbRfdptazxw&usqp=CAU"/>'
            folium.Marker(
                    location=cord,
                    tooltip="Demo Plot",
                    popup = pop_info,
                    icon=folium.Icon(color="green"),
                    ).add_to(cluster)
    cluster.add_to(feature_group)
    feature_group.add_to(map)