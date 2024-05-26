# moderation.py

import nextcord
from nextcord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members.")

    @commands.command(name="unban", description="Unban a member by their user ID or username#discriminator")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user_info):
        banned_users = await ctx.guild.bans()
        user_name, user_discriminator = user_info.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')
                return

        await ctx.send(f'User {user_info} not found in the ban list.')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to unban members.")
        elif isinstance(error, ValueError):
            await ctx.send("Invalid user format. Please use the format `username#discriminator`.")

    @commands.command(name="kick", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick members.")

    @commands.command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: nextcord.Member, *, reason=None):
        muted_role = nextcord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'{member.mention} has been muted.')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to mute members.")

    @commands.command(name="warn", description="Warn a member")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: nextcord.Member, *, reason=None):
        # You can implement your warning logic here, like logging the warning, sending a DM to the user, etc.
        await ctx.send(f'{member.mention} has been warned for {reason}.')

def setup(bot):
    bot.add_cog(Moderation(bot))
