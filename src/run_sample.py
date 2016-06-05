import asyncio

from bot import SpeckChecker

if __name__ == "__main__":
    token = "TOKEN_HERE"
    channel_id = "CHANNEL_ID"
    event_id = "STEAM_EVENT_ID"

    testBot = SpeckChecker(token, channel_id, event_id)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(testBot.checkEvents())
        loop.run_until_complete(testBot.login(testBot.token))
        loop.run_until_complete(testBot.connect())
    except Exception as e:
        loop.run_until_complete(testBot.close())
    finally:
        loop.close()
