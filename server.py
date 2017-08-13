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

lyrics = ["If you need to crash, then crash and burn, you're not alone.",
          "Let me be the one you call. If you jump, I'll break your fall.",
          "Give me a moment please to tame your wild wild heart.",
          "If you need to fall apart, I can mend a broken heart.",
          "There has always been heartache and pain. When it's over you'll breathe again."]

emoji = ["😇",
         "😘",
         "👍",
         "💖"]

async def handle(request):
    """Respond to incoming requests."""

    response = VoiceResponse()
    # By calling functions on gather, digits can be pressed during the song
    # playback *and* the menu afterwards.
    city = request.GET.get("CallerCity")
    state = request.GET.get("CallerState")
    if city and state:
        update_status(city, state)
    response.play('https://s3.ca-central-1.amazonaws.com/strangerelationship/Savage+Garden+-+Crash+And+Burn.mp3')

    # Our goodbye triggers after gather times out.
    response.say("Thanks for calling!")

    return web.Response(text=str(response), content_type='application/xml')

def update_status(city, state):

    message = f"😊 Thanks for dialing in, caller from {city}, {state}. {random.choice(lyrics)} {random.choice(emoji)}"
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