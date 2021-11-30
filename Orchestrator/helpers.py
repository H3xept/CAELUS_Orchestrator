

def validate_docker_image(data):
    return True

def validate_mission(data):
    return all(map(lambda x: x in data, ['waypoints', 'operation_id', 'control_area_id', 'operation_reference_number', 'drone_id', 'drone_registration_number', 'dis_auth_token', 'thermal_model_timestep', 'aeroacoustic_model_timestep', 'drone_config', 'g_acceleration', 'initial_lon_lat_alt']))

def validate_payload(payload):
    if payload is None:
        return False
    return not (payload is None or 'docker_img' not in payload or 'mission' not in payload) and \
    (validate_docker_image(payload['docker_img'])) and \
    (validate_mission(payload['mission']))
