import nextcord
from nextcord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, ctx, member: nextcord.Member = None):
        member = member or ctx.author

        embed = nextcord.Embed(title=f"User Info - {member}", color=0x00ff00)

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="Discriminator", value=member.discriminator)
        embed.add_field(name="Bot", value=member.bot)
        embed.add_field(name="Created At", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"))
        
        if member.joined_at:
            embed.add_field(name="Joined At", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"))

        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        embed.add_field(name=f"Roles [{len(roles)}]", value=" ".join(roles) if roles else "None")

        await ctx.send(embed=embed)

    @commands.command(name="membercount", description="Display the total number of members in the server")
    async def membercount(self, ctx):
        member_count = ctx.guild.member_count
        embed = nextcord.Embed(title="Member Count", description=f"Total Members: {member_count}", color=0x00ff00)
        await ctx.send(embed=embed)
    
    @commands.command(name="info", description="Get information about the bot")
    async def info(self, ctx):
        embed = nextcord.Embed(title="Bot Information", description="This bot provides various functionalities.", color=0x00ff00)
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=False)
        embed.add_field(name="Owner", value="OWNER_USERNAME", inline=False)  # Replace "Your Name Here" with your name or username
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Bot Invite Link", value= "BOT_INVITE_LINK", inline=False)  # Replace "Your Bot Invite Link Here" with your bot's invite link
        await ctx.send(embed=embed)
    
    @commands.command(name="avatar", description="Get the avatar of a user")
    async def avatar(self, ctx, user: nextcord.Member = None):
        if user is None:
            user = ctx.author

        embed = nextcord.Embed(title=f"{user.name}'s Avatar", color=0x00ff00)
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="poll", description="Start a poll (requires manager permissions)")
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question, *options):
        if len(options) > 10:
            await ctx.send("You can only provide up to 10 options for the poll.")
            return

        # Create embed message for the poll
        embed = nextcord.Embed(title="Poll", description=question, color=0x00ff00)
        for i, option in enumerate(options, start=1):
            embed.add_field(name=f"Option {i}", value=option, inline=False)

        # Send the poll message
        message = await ctx.send(embed=embed)

        # Add reactions for each option
        for i in range(len(options)):
            await message.add_reaction(chr(0x1F1E6 + i))

def setup(bot):
    bot.add_cog(Utility(bot))
