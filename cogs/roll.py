# roll.py

import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import random

class RollView(View):
    def __init__(self, ctx, timeout=300):
        super().__init__(timeout=timeout)
        self.ctx = ctx  # Store the context (message) of the command
        self.user = ctx.author.id  # Store the ID of the user who initiated the command

    @nextcord.ui.button(label="Roll", style=nextcord.ButtonStyle.primary)
    async def roll_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Check if the interaction is from the same user who initiated the command
        if interaction.user.id != self.user:
            await interaction.response.send_message("You cannot roll the dice for someone else!", ephemeral=True)
            return

        # If it's the same user, proceed to roll the dice
        dice_result = random.randint(1, 100)
        await interaction.response.send_message(f'You rolled a {dice_result}!', ephemeral=True)

class RollDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", description="Roll a number 1-100")
    async def rolldice(self, ctx):
        view = RollView(ctx)
        await ctx.send("Click the button to roll the dice!", view=view)

def setup(bot):
    bot.add_cog(RollDice(bot))
