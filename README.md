# Discord-Selfbot-Framework
A simple discord framework for managing regular accounts via gateway and http api
Using this, you can manage gateway events, process commands, using discord message components and etc.
For example, this is simple snippet of code, that provides simple framework usage
```python
from bot import Bot
from models import Message, Context

bot = Bot ("TOKEN", "COMMAND_PREFIX")

@bot.event("MESSAGE_CREATE")
async def on_message(message: Message):
  ...
  await bot.process_commands(message)

@bot.command("ping")
async def ping(context: Context):
  await context.reply("pong!")

bot.run()
```
also you can create commands with strict-type args using annotations
```python
@bot.command("echo")
async def echo(context: Context, text: str):
  await context.reply(text)

@bot.command("plus")
async def plus(context, left_operand: float, right_operand: float):
  await context.reply(str(left_operand + right_operand))
```
adding reactions and using message components (buttons, lists) are supported too
```python
@bot.command("react_me")
async def react_me(context, emoji: str):
  await context.add_reaction(f"{emoji}")

@bot.command("unbelieva_blackjack")
async def unbelieva_blackjack(context, prefix: str, bet: int):
  await context.send(f"{prefix}bj {bet}")
  # example of getting bot message (event waiting will be added in future)
  message = await bot.get_messages((await context.channel()).id, limit = 1)[0]
  # click "hit" button
  # first is components row, second is row component
  await message.components[0].components[0].click()
```

full docs on readthedocs soon (: