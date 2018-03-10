
import os
import logging

import alexa
from teamcowpy import teamcowpy
import yaml


with open('templates.yaml', 'r') as f:
    templates = yaml.load(f)


def lambda_handler(event, context):
    req_type = str(event['request']['type'])
    print "request type: " + req_type

    if str(req_type) == "LaunchRequest":
        res = on_launch(event, context)
        print res
        return res

    elif req_type == "IntentRequest":
        return intent_router(event, context)

    elif req_type == "SessionEndedRequest":
        return event

    return intent_router(event, context)


def on_launch(event, context):
    print("On Launch")
    return alexa.build_response(
        session_attributes={"test": "testvalue"},
        speechlet_response= alexa.build_speechlet_response(
            title="Vipers",
            output=alexa.build_speech_output("Hi there vipers fan. What sort of info are you looking for?"),
            reprompt_text="What sort of info are you looking for?",
            should_end_session=False
        )
    )


def intent_router(event, context):
    intent = str(event['request']['intent']['name'])

    # Custom Intents
    print "Intent: " + str(intent)
    if intent == "getNextGame":
        return getNextGame(event, context)

    # if intent == "SingIntent":
    #     return sing_intent(event, context)
    #
    # if intent == "TripIntent":
    #     return trip_intent(event, context)

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()

    if intent == "AMAZON.YesIntent":
        last = str(event["session"]['attributes']['lastIntent'])
        if last == "nextGame":
            return getNextGame(event, context)

    if intent == "AMAZON.NoIntent":
        if 'lastIntent' in event["session"]['attributes'].keys():
            last = str(event["session"]['attributes']['lastIntent'])
            if last == "nextGame":
                return cancel_intent()

##############################
# Required Intents
##############################


def cancel_intent():
    say = templates['cancel']
    reprompt = None
    endSession = True
    return alexa.build_response({},
                                alexa.build_speechlet_response("Bye",
                                                               alexa.build_speech_output(say),
                                                               reprompt,
                                                               endSession))


def help_intent():
    return "CancelIntent", "You want help"		#same here don't use CancelIntent


def stop_intent():
    return "StopIntent", "You want to stop" #here also don't use StopIntent


##############################
# Skill Intents
##############################

#@ask.intent('getNextGame')
def getNextGame(event, context):
    API_KEYS = {
        "public": os.getenv('tc_api_public'),
        "private": os.getenv('tc_api_private')
    }
    if 'attributes' in event['session']:
        if "nextGameIteration" in event["session"]['attributes']:
            i = int(event["session"]['attributes']['nextGameIteration'])
        else:
            i = 0
    else:
        i = 0

    tc = teamcowpy.User(keys=API_KEYS, u=os.getenv('tc_username'), p=os.getenv('tc_password'))
    evts = tc.getTeamEvents()

    games = [{'team': e['team']['name'],
              'date': e['dateTimeInfo']['startDateTimeLocalDisplay'],
              'opponent': e['title'],
              'location': e['location']['name']} for e in evts if not e['dateTimeInfo']['inPast']]

    game = games[i]
    if game['team'] == "Vipers Hockey Club":
        game['team'] = "Vipers Five"

    say = templates['nextGame'].format(location=game['location'],
                                       opponent=game['opponent'],
                                       day=game['date'],
                                       team=game['team'])

    i = i + 1
    if i > 3:
        say = templates['nextGameDone']
        reprompt = None
        endSession = True
    else:
        reprompt = templates["nextGameReprompt"]
        endSession = False

    return alexa.build_response({'nextGameIteration': i, 'lastIntent': 'nextGame'},
                                alexa.build_speechlet_response("NextGame",
                                                               alexa.build_speech_output(say, True),
                                                               reprompt,
                                                               endSession))


# @ask.launch
# def launch():
#     speech_text = 'Welcome to the Alexa Skills Kit, you can say. Pick a place for me in New York'
#     return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

# @ask.intent('RestaurantByCityIntent')
# def get_restuarant_by_city(USCitySlot):
#     return search (USCitySlot)
if __name__ == '__main__':
    print(alexa.build_speech_output("hello", True))