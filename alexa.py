



############### HELPERS #####################
def build_speechlet_response(title, output, reprompt_text, should_end_session):

    return {
        'outputSpeech': output,
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output['text']
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def build_speech_output(verbage,ssml=False):
    speech = {}
    speech['type'] = 'SSML' if ssml else 'PlainText'
    speech['text'] = verbage
    if ssml:
        speech['ssml'] = verbage

    return speech