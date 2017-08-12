import os
from aiohttp import web
# from twilio.twiml.voice_response import VoiceResponse


async def handle(request):
    """Respond to incoming requests."""

    # response = VoiceResponse()
    #
    # # By calling functions on gather, digits can be pressed during the song
    # # playback *and* the menu afterwards.
    # # gather = response.gather(numDigits=1, timeout=10)
    # # gather.play('https://www.youtube.com/watch?v=W60IPexop30')
    #
    # # Our goodbye triggers after gather times out.
    # response.say("Thanks for calling the Crash and Burn hotline. Good bye!")

    # # return str(resp)
    return web.Response(text="Hello")

app = web.Application()
app.router.add_get('/', handle)

port = os.environ.get("PORT")
if port is not None:
    port = int(port)
web.run_app(app, host="http://0.0.0.0", port=port)