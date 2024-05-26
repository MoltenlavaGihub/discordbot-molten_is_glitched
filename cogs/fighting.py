import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import random

class FightingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fightdummy", description="Start a fight with the bot!")
    async def fight(self, ctx):
        embed = nextcord.Embed(title="Fight!", description="React with the attack you want to perform.", color=0x00ff00)
        message = await ctx.send(embed=embed, view=FightingView())
        await message.add_reaction("💥")
        await message.add_reaction("👊🏿")
        await message.add_reaction("❌")

class FightingView(View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Punch", style=nextcord.ButtonStyle.primary, custom_id="punch")
    async def punch(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You punched the opponent!", ephemeral=True)

    @nextcord.ui.button(label="Kick", style=nextcord.ButtonStyle.danger, custom_id="kick")
    async def kick(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You kicked the opponent!", ephemeral=True)

    @nextcord.ui.button(label="Block", style=nextcord.ButtonStyle.secondary, custom_id="block")
    async def block(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You blocked the opponent's attack!", ephemeral=True)

def setup(bot):
    bot.add_cog(FightingCog(bot))
