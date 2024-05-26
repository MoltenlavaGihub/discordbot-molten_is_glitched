# fun.py

import nextcord
from nextcord.ext import commands
import random
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_guild_commands(self, guild_id):
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            return []

        commands = []

    @commands.command(name="joke", description="Tell a random joke")
    async def joke(self, ctx):
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke_data = response.json()
            joke_text = f"{joke_data['setup']} - {joke_data['punchline']}"
            await ctx.send(joke_text)
        else:
            await ctx.send("Couldn't fetch a joke at this moment, please try again later.")

    @commands.command(name="funfact", description="Tell a random fun fact")
    async def funfact(self, ctx):
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            fact_data = response.json()
            fact_text = fact_data['text']
            await ctx.send(fact_text)
        else:
            await ctx.send("Couldn't fetch a fun fact at this moment, please try again later.")

    @commands.command(name="flag", description="Show a random country flag")
    async def flag(self, ctx):
        response = requests.get("https://restcountries.com/v3.1/all")
        if response.status_code == 200:
            countries = response.json()
            random_country = random.choice(countries)
            country_name = random_country['name']['common']
            flag_url = random_country['flags']['png']
            embed = nextcord.Embed(title=country_name, color=0x1ABC9C)
            embed.set_image(url=flag_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't fetch a country flag at this moment, please try again later.")

    @commands.command(name="rip", description="Output a grave clip art and the provided text")
    async def rip(self, ctx, *, text: str):
        embed = nextcord.Embed(title="RIP", description=text, color=0x000000)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1210787573014986764/1243838409303130202/background-remove.png?ex=6652ee4a&is=66519cca&hm=50c663d2fcaac9e1b5830b41dd1595bfdf97cf6c7edd8b3cf8ad068bd04124d6&")  # URL of the grave clip art image
        await ctx.send(embed=embed)

    @commands.command(name="flaggame", description="Guess the country flag!")
    async def flaggame(self, ctx):
        # Fetch a list of all countries with their flags
        response = requests.get("https://restcountries.com/v3.1/all")
        if response.status_code == 200:
            countries = response.json()
            # Choose a random country and its flag
            random_country = random.choice(countries)
            country_name = random_country['name']['common']
            flag_url = random_country['flags']['png']
            # Send the flag image to the user
            await ctx.send(f"Guess the country flag! What country does this flag belong to?\n{flag_url}")

            def check(message):
                # Check if the message is from the same user who initiated the command and it's not a bot message
                return message.author == ctx.author and not message.author.bot

            try:
                # Wait for the user's guess
                guess = await self.bot.wait_for('message', check=check, timeout=30)
                # Check if the guess is correct
                if guess.content.lower() == country_name.lower():
                    await ctx.send(f"Correct! {country_name} is the correct answer.")
                else:
                    await ctx.send(f"Sorry, the correct answer was {country_name}. Try again next time!")
            except nextcord.TimeoutError:
                await ctx.send("Time's up! You didn't answer in time.")

        else:
            await ctx.send("Couldn't fetch country flags at this moment, please try again later.")

def setup(bot):
    bot.add_cog(Fun(bot))
