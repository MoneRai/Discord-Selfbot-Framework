# Discord-Selfbot-Framework
<div align = "center">
  <a href = "https://www.python.org/downloads/release/python-31011/"><img src = "https://img.shields.io/badge/python-3.10-red.svg?logo=python"></a>
  <a href = ""><img src = "https://img.shields.io/badge/pypi-none-red?logo=pypi"></a>
  <a href = ""><img src = "https://img.shields.io/badge/readthedocs-none-red?logo=readthedocs"></a>
  <a href = "https://github.com/MoneRai/Discord-Selfbot-Framework/releases/tag/Beta"><img src = "https://img.shields.io/badge/release-1.0-red?logo=github"></a>
</div>

A simple discord framework for managing regular accounts via gateway and HTTP API.

Using this, you can manage gateway events, process commands, use discord message components and etc.
For example, this is simple snippet of code, that provides simple framework usage
```python
from bot import Bot
from models import Message, Context

bot = Bot("TOKEN", "COMMAND_PREFIX")

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
  # example of waiting for event
  message = await bot.wait_for("MESSAGE_CREATE", check = lambda m: m.author.id == ...)
  # click "hit" button
  await message.rows[0].components[0].click()
```

single (non-group, i'm too lazy to do slash command groups) slash commands usage 
```python
@bot.command("slash")
async def slash(context):
  await context.send_slash_command("cat", ())
```
where empty tuple is slash command options. Slash command with options usage:
```python
@bot.command("slash")
async def slash(context):
  await context.send_slash_command("cat", (("url", "https://..."), ("number": 4)))
```

full docs on readthedocs is soon (no more than 100 years)