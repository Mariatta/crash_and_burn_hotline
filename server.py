import os
from aiohttp import web
from twilio.twiml.voice_response import Play, VoiceResponse


async def handle(request):
    """Respond to incoming requests."""

    response = VoiceResponse()

    # By calling functions on gather, digits can be pressed during the song
    # playback *and* the menu afterwards.
    response.say("Hello ")
    response.play('http://demo.twilio.com/hellomonkey/monkey.mp3')

    # Our goodbye triggers after gather times out.
    # response.say("Thanks!")
    print(response)
    # # return str(resp)
    return web.Response(text=str(response))

app = web.Application()
app.router.add_get('/', handle)

port = os.environ.get("PORT")
if port is not None:
    port = int(port)
web.run_app(app, port=port)