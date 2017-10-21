import os
import random
from aiohttp import web
from twilio.twiml.voice_response import VoiceResponse
from twython import Twython

twitter = Twython(
    os.getenv("TW_API_KEY"),
    os.getenv("TW_API_SECRET"),
    os.getenv("TW_ACCESS_TOKEN"),
    os.getenv("TW_TOKEN_SECRET")
)

emoji = ["😇",
         "😘",
         "👍",
         "💖"]

MUSIC_COLLECTION = [
    {'title': 'Crash and Burn',
     'selected_lyrics': [
         "If you need to crash, then crash and burn, you're not alone.",
         "Let me be the one you call. If you jump, I'll break your fall.",
         "Give me a moment please to tame your wild wild heart.",
         "If you need to fall apart, I can mend a broken heart.",
         "There has always been heartache and pain. When it's over you'll breathe again."
     ],
     'url': 'https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden+-+Crash+And+Burn.mp3',
     },
    {'title': 'I Want You',
     'selected_lyrics': [
         "Anytime I need to see your face I just close my eyes.",
         "Ooh I want you, I don't know if I need you, but ooh, I'd die to find out.",
         "I'm the kind of person who endorses a deep commitment.",
         "It's like I'm down on the floor and I don't know what I'm in for.",
         "Using words can be likened to a deep sea diver who is swimming with a raincoat."
     ],
     'url': 'https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden+-+I+Want+You.mp3',
     },
    {'title': 'Truly, Madly, Deeply',
     'selected_lyrics': [
         "I'll be your dream, I'll be your wish, I'll be your fantasy.",
         "I'll be your hope, I'll be your love, be everything that you need.",
         "I love you more with every breath, truly madly deeply do.",
         "I will be strong, I will be faithful 'cause I'm counting on a new beginning.",
         "I want to lay like this forever. Until the sky falls down on me."
     ],
     'url': 'https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden+-+Truly+Madly+Deeply.mp3',
     },
    {'title': 'To The Moon and Back',
     'selected_lyrics': [
         "I would fly to the moon and back.",
         "I've got a ticket for a world where we belong.",
         "Love is like a barren place.",
         "Reaching out for human faith is like a journey I just don't have a map for.",
         "Waiting for the right kind of pilot to come."
     ],
     'url': 'https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden+-+To+The+Moon+%26+Back+(Extended+Version).mp3',
     },
     {'title': 'The Best Thing',
     'selected_lyrics': [
         "Frightened to believe: you're the best thing all about me.",
         "Walk on broken glass, make my way through fire. These are things I would do for love.",
         "Never want to fly, never want to leave. Never want to say what you mean to me.",
         "You're the center of adrenalin. And I'm beginning to understand.",
     ],
     'url': 'https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden-+The+Best+Thing+Lyrics.mp3',
     },
]


async def handle(request):
    """Respond to incoming requests."""

    response = VoiceResponse()
    state = request.GET.get("FromState")

    selected_music = random.choice(MUSIC_COLLECTION)
    selected_lyric = random.choice(selected_music['selected_lyrics'])
    update_status(state, selected_lyric)
    response.play(selected_music['url'])

    response.say("Thanks for calling!")

    return web.Response(text=str(response), content_type='application/xml')


def update_status(state=None, selected_lyric=''):

    from_phrase = ""
    if state:
        from_phrase = f", caller from {state}"

    message = f"😊 Thanks for dialing in{from_phrase}. {selected_lyric} {random.choice(emoji)}"
    if len(message) > 140:
        twitter.update_status(status=message[0:140])
    else:
        twitter.update_status(status=message)


app = web.Application()
app.router.add_get('/', handle)

port = os.environ.get("PORT")
if port is not None:
    port = int(port)
web.run_app(app, port=port)
