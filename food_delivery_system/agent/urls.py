from django.urls import path,include
from agent.views import AgentAPI


urlpatterns = [
    path('agent_api/',AgentAPI.as_view()),
]