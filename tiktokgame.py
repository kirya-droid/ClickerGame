from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent

# Instantiate the client with the user's username

client: TikTokLiveClient = TikTokLiveClient(unique_id="@jtxqylzysb2")


# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")

@client.on("like")
async def on_like(event: LikeEvent):
    print(f"@{event.user.unique_id} liked the stream!")

# Define handling an event via a "callback"
client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
