import logging

from flask import Flask
from flask_ask import Ask, question, statement
from api import search


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)

def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents

    if intent == "CounterIntent":
        return counter_intent(event, context)

    if intent == "SingIntent":
        return sing_intent(event, context)

    if intent == "TripIntent":
        return trip_intent(event, context)

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()

##############################
# Required Intents
##############################


def cancel_intent():
    return statement("CancelIntent", "You want to cancel")	#don't use CancelIntent as title it causes code reference error during certification


def help_intent():
    return statement("CancelIntent", "You want help")		#same here don't use CancelIntent


def stop_intent():
    return statement("StopIntent", "You want to stop") #here also don't use StopIntent


##############################
# Skill Intents
##############################

@ask.intent('getNextGame')
def getNextGame():


@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say. Pick a place for me in New York'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('RestaurantByCityIntent')
def get_restuarant_by_city(USCitySlot):
    return search (USCitySlot)


if __name__ == '__main__':
    tc =