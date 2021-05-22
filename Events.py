import os
import discord
from discord.ext import commands
from dotenv.main import load_dotenv
from utils import GameGrid
from imgurpython import ImgurClient

load_dotenv()

imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')

imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

class Events:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",
                               description=f"Try again in {error.retry_after:.2f}s.\n The default cooldown is {error.cooldown.per}s",
                               color=discord.Color.red())
            await ctx.send(embed=em)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title=':x: oops! You do not have permission to use this command.',
                                  color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=':x: You are missing the required arguments. Please check if your command requires an addition arguement.',
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title=':x: Chintu is missing the required permissions. Please check if Chintu has appropriate permissions.',
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title=':x: Could not find the mentioned user. Please mention a valid user.',
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=':x: Enter a valid argument',
                color=discord.Colour.red())
            await ctx.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        message = reaction.message

        if GameGrid.getGamesByUser(str(user.id)) is not None:
            game = GameGrid.getGamesByUser(str(user.id))
            if str(game.getMessageId()) == str(message.id):
                if str(reaction.emoji) == '⬆':
                    game.slideUp()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '⬇':
                    game.slideDown()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '➡':
                    game.slideRight()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '⬅':
                    game.slideLeft()
                    game.randomNumber()
                    game.drawMatrix()

                game.saveImage(str(user.id))
                img = imgur_client.upload_from_path(game.temp + f'{user.id}.png')
                try:
                    os.remove(game.temp + f'{user.id}.png')
                except Exception:
                    pass

                await message.remove_reaction(reaction, user)

                embed = discord.Embed(title='2048', color=discord.Color.dark_theme())
                embed.set_image(url=str(img['link']))
                message = await message.edit(embed=embed)
