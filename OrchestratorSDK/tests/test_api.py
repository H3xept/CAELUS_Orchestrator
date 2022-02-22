from dotenv import load_dotenv
from os import environ
import logging
import pytest

from Orchestrator.api import OrchestratorAPI, Account

load_dotenv('.env.test')
logging.basicConfig(level=logging.INFO)

latest_job_id = None
ORCHESTRATOR_API_URL = environ.get('ORCHESTRATOR_API_URL')
DEFAULT_ADMIN_PASSWORD = environ.get('DEFAULT_ADMIN_PASSWORD')

def test_register():
    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    admin_account = api.authenticate('admin', DEFAULT_ADMIN_PASSWORD)
    assert api.register('new_user', 'test', admin_account)
    
def test_login():
    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    assert api.authenticate('new_user', 'test') is not None

def test_get_activated_jobs():
    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    account = api.authenticate('new_user', 'test')
    activated_jobs = api.get_activated_jobs(account).json()
    assert type(activated_jobs) == list
    


def test_get_pending_jobs():
    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    account = api.authenticate('new_user', 'test')
    assert api.get_pending_jobs(account).json() == []

def test_schedule_new_mission():
    global latest_job_id
    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    account = api.authenticate('new_user', 'test')
    test_mission = {
    "waypoints": [
        [-4.235670388, 55.8640195695, 143.4014020115818],
        [-4.249079040000051, 55.864360463000224, 154.98323681804328],
        [-4.262487695999948, 55.86470135699977, 154.98323681804328],
        [-4.2758963530000536, 55.865042250000236, 149.95428223102712],
        [-4.289305008999948, 55.865383143999765, 135.93416641267908],
        [-4.302713665000051, 55.86572403700022, 124.50472416946053],
        [-4.316122320999948, 55.86606493099977, 119.01859189271563],
        [-4.329530977000001, 55.866405824, 122.52362084730265],
        [-4.342939633000051, 55.86674671700022, 124.50472416946053],
        [-4.356348289999949, 55.867087610999775, 122.98079853703139],
        [-4.369756946000052, 55.86742850400023, 123.59036879000304],
        [-4.3831656019999485, 55.86776939799978, 124.1999390429747],
        [-4.396574258, 55.868110291, 124.65711673270343],
        [-4.409982914000052, 55.86845118400023, 127.09539774459006],
        [-4.423391569999961, 55.86879207799983, 125.57147211216092],
        [-4.434627022520515, 55.86907701039248, 120.54251752514477],
        [-4.435110004, 55.8690899995, 103.47455044193843],
        [-4.435110004, 55.8690899995, 27.125876257238644]
    ],
    "operation_id": "cf202c29-855d-4dfa-ba69-a516cc4249dd",
    "control_area_id": "2eee4ddf-b230-4be1-aee0-0a827e818fa5",
    "operation_reference_number": "7640b36a-3c6a-43f5-8416-ab3750370d74",
    "drone_id": "769ca9b2-88eb-47f2-b417-fe6d693745a0",
    "drone_registration_number": "4df75a49-a927-487a-adaf-2e54282241f2",
    "dis_auth_token": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJaR2w3MjFlODhJenB3ZUJpZ1lESkl6UEY2OExHVDJrajYtNzFweGE2ZUEwIn0.eyJleHAiOjE2NDU1MzQxMzEsImlhdCI6MTY0NTUzMDUzMSwianRpIjoiNDFiYjQxZTAtZTZhYS00OWM3LWI3MDUtMDAyNmZiZTc4ODRiIiwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mbHlhbnJhLm5ldC9hdXRoL3JlYWxtcy9BTlJBIiwiYXVkIjpbIkFucmFUZWNobm9sb2dpZXMiLCJTUy1DVFIiLCJhY2NvdW50Il0sInN1YiI6Ijc0MjYyYWFiLTg2YzgtNGRkOS1iYmRiLTA2MTcxMGY0ZGJjNCIsInR5cCI6IkJlYXJlciIsImF6cCI6IkRNUyIsInNlc3Npb25fc3RhdGUiOiI4YzU5YWU0OS0zMDJiLTQ2ODQtOTM5My0xN2IwMjVmMjdhZTciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIkxheWVyTWFuYWdlcl9SZWFkT25seSJdfSwicmVzb3VyY2VfYWNjZXNzIjp7IlNTLUNUUiI6eyJyb2xlcyI6WyJQSUxPVCIsIkFETUlOIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJ3ZWJzaXRlIjoiIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJESVMgQWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbkBkaXMudGVzdCIsImdpdmVuX25hbWUiOiJESVMiLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiZW1haWwiOiJhZG1pbkBkaXMudGVzdCJ9.LRh05idPQf5GxnNMpr_i0rSqeEvVmLlOZsQS2w5AC9jgAqQayhqE2MaIvKWDF5Kmie4C9mKaQYtnANMghzKxle0KRO0te1coi2hTBNhwXbgZ7KX_rtB0HfURsMu3cPivscnk0GoMCwjaBBUEm7hlL48MQL7VWEQCXfZBit8hr85NioP61c0vppGhg3pjmoOSEGgapZpweUAr6pGEvntqb95Z2XI0BXhd0BduvtXr8R4pK9AIJJ9SpHE77npKjmu9H5L7jLSbTRJMXVpMCOp06LWPT7NQul_Tlii6yjdnR4eJo1c0VJnuY9pcfkgJ77M9QGGU0BwJr3nc4rNKKWEUuA",
    "dis_refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyYzYwODkzZi00MTIwLTRjNDgtYjc2Zi04ODJiZDI2YTMzMGEifQ.eyJleHAiOjE2NDU2MTY5MzEsImlhdCI6MTY0NTUzMDUzMSwianRpIjoiYmEzNWU4ZWYtYzZmMS00YTE4LTg1ODktN2Q5NzIzMDNkMTA3IiwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mbHlhbnJhLm5ldC9hdXRoL3JlYWxtcy9BTlJBIiwiYXVkIjoiaHR0cHM6Ly9vYXV0aC5mbHlhbnJhLm5ldC9hdXRoL3JlYWxtcy9BTlJBIiwic3ViIjoiNzQyNjJhYWItODZjOC00ZGQ5LWJiZGItMDYxNzEwZjRkYmM0IiwidHlwIjoiUmVmcmVzaCIsImF6cCI6IkRNUyIsInNlc3Npb25fc3RhdGUiOiI4YzU5YWU0OS0zMDJiLTQ2ODQtOTM5My0xN2IwMjVmMjdhZTciLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUifQ.XCIvxSv-qDkTeS7fIqhjG7aGLxV7UkbYYaUhDCNIhKg",
    "cvms_auth_token": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJaR2w3MjFlODhJenB3ZUJpZ1lESkl6UEY2OExHVDJrajYtNzFweGE2ZUEwIn0.eyJleHAiOjE2NDU1MzQxMzIsImlhdCI6MTY0NTUzMDUzMiwianRpIjoiY2Y0ZjNlNzAtNGU2MS00MThjLTg5YWQtYzc3ZDNlNTM2ODAzIiwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mbHlhbnJhLm5ldC9hdXRoL3JlYWxtcy9BTlJBIiwiYXVkIjpbIkFucmFUZWNobm9sb2dpZXMiLCJhY2NvdW50Il0sInN1YiI6Ijk5MDJlNGJmLTliZmMtNGYwMi05MjVhLWY1ZDFjNjk1OWU0ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6IkRNUyIsInNlc3Npb25fc3RhdGUiOiIyMmJhNzkxNC1lMGQyLTQ2MTktYTFlMy00MDAwY2Y0NGEwNjAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkdsYXNnb3cgQWlycG9ydCAoaHViIHBvaW50KSwgY3VzdG9tZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIrMS0wODMtOTg3LTUyNjYiLCJnaXZlbl9uYW1lIjoiR2xhc2dvdyBBaXJwb3J0IChodWIgcG9pbnQpLCBjdXN0b21lciIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJjMzNlOWUwQGdtYWlsLmNvbSJ9.V4eqBx9tIlN9K55VikDVUdbEnrbcYi2zU7TY1-LZn6z4dLUeK_-eAUmtjW8zuC3AHA4iYm623uCiD6hBb84iU2-GKiCG3cAw44mroG2tZ62DP4oYx9sdSgkG6DVQN49_9nVrl4eUwM6xmTC96hjvxPLWg9WsSIXQ_sltgCHk5CLznbi6QZqlIyKsHrq13rXzEKxYq-Dn0Vkg5l89tjufqSuXWiwgx1YwijWyWvNL4UyvKxfV7gW33mDd4DW0gbi4ccJMjfkEPTAHoKGtVwL3tpVyOm4eF8mIeWXeNQeXsHJy3T6S-jeirAIGL2N_d9BHQZ7vHkiCzZTNvjXf05zFFg",
    "delivery_id": "8a38316a-92ad-4320-8bbd-9fc3507c7353",
    "thermal_model_timestep": 1,
    "aeroacoustic_model_timestep": 0.004,
    "drone_config_file": "evtol_fw_large.json",
    "payload_mass": 0.25,
    "g_acceleration": 9.81,
    "group_id": "test_orchestrator_sdk",
    "effective_start_time": 1645530736.069071,
    "initial_lon_lat_alt": [-4.235670388, 55.8640195695, 67.55272782688205],
    "final_lon_lat_alt": [-4.435110004, 55.8690899995, 27.125876257238644]
    }
    response = api.schedule_new_mission(test_mission, account=account).json()
    assert 'job_id' in response and response['job_id'] is not None
    latest_job_id = response['job_id']

import time

def test_halt_mission():
    """
    Test halting a mission
    """

    # Bad practice - but I need to wait for the orchestrator to launch the mission
    time.sleep(2)
    # ---

    api = OrchestratorAPI(ORCHESTRATOR_API_URL)
    account = api.authenticate('new_user', 'test')
    response = api.halt_mission(latest_job_id, account=account)
    assert response.status_code == 200
