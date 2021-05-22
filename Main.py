import os
import discord
from dotenv import load_dotenv
from Events import Events
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=">", description="2048 Bot", intent=discord.Intents().all())
TOKEN = os.getenv('TOKEN')


@bot.event
async def on_ready():
    print("Bot started!")
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


@bot.command(name="extension")
async def extension(ctx, args, cog):
    file = f'{cog}.py'
    if args == 'load':
        if file not in os.listdir("./cogs"):
            embed = discord.Embed(title="Error",
                                  description="The given extension not found!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        bot.load_extension(f"cogs.{cog}")
        embed = discord.Embed(title=f"Loaded {cog}",
                              description="Extension loaded successfully!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    elif args == 'unload':
        if file not in os.listdir("./cogs"):
            embed = discord.Embed(title="Error",
                                  description="The given extension not found!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        bot.unload_extension(f"cogs.{cog}")
        embed = discord.Embed(title=f"Unloaded {cog}",
                              description="Extension unloaded successfully!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    elif args == 'reload':
        if file not in os.listdir("./cogs"):
            embed = discord.Embed(title="Error",
                                  description="The given extension not found!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")

        embed = discord.Embed(title=f"Reloaded {cog}",
                              description="Extension reloaded successfully!",
                              color=discord.Color.green())
        await ctx.send(embed=embed)


bot.event(Events(bot).on_command_error)
bot.event(Events(bot).on_reaction_add)


def load_extensions(fun_bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            fun_bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    print('Loading extensions...')
    load_extensions(bot)
    print('Logging in...')
    bot.run(TOKEN)
