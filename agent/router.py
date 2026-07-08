from agent.providers.google.api import messageGoogle
from agent.providers.groq.api import messageGroq
from agent.features.launch import launch
from agent.features.greet import greet
from agent.config import PROVIDER , SYSTEM

class Router:



providers = {
    "google" : messageGoogle,
    "groq" : messageGroq
}
actions = {
    "launch" : launch,
    "greet" : greet,
}



