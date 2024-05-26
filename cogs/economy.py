import nextcord
from nextcord.ext import commands
import random
from datetime import datetime, timedelta
from nextcord.ext.commands import cooldown, BucketType


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = {}
        self.jobs = {
            "Teacher": 50,
            "Developer": 100,
            "Doctor": 150,
            "Chef": 70,
            "Pilot": 200
        }
        self.daily_streaks = {}
        self.last_claimed = {}
        self.user_jobs = {}  # Dictionary to track users' job applications
        self.job_application_times = {}  # Dictionary to track the last time a user applied for a job
        self.shop_items = {
            "Apple": 10,
            "Sword": 100,
            "Shield": 150,
            "Potion": 50,
            "Book": 30
        }
        self.user_inventories = {}  # Dictionary to track users' inventories

    def get_balance(self, user_id):
        return self.balances.get(user_id, 0)

    def add_balance(self, user_id, amount):
        if user_id in self.balances:
            self.balances[user_id] += amount
        else:
            self.balances[user_id] = amount

    def subtract_balance(self, user_id, amount):
        if user_id in self.balances:
            self.balances[user_id] = max(0, self.balances[user_id] - amount)

    def add_item(self, user_id, item_name):
        if user_id not in self.user_inventories:
            self.user_inventories[user_id] = {}
        if item_name in self.user_inventories[user_id]:
            self.user_inventories[user_id][item_name] += 1
        else:
            self.user_inventories[user_id][item_name] = 1

    @commands.command(name="balance", aliases=["bal"], description="Check your balance")
    async def balance(self, ctx):
        user_id = ctx.author.id
        balance = self.get_balance(user_id)
        embed = nextcord.Embed(title=f"{ctx.author.name}'s Balance", description=f"You have {balance} coins.", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="earn", description="Earn some coins")
    async def earn(self, ctx):
        user_id = ctx.author.id
        amount = random.randint(10, 100)
        self.add_balance(user_id, amount)
        embed = nextcord.Embed(title="Earned Coins", description=f"You earned {amount} coins!", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="spend", description="Spend some coins")
    async def spend(self, ctx, amount: int):
        user_id = ctx.author.id
        if amount <= 0:
            await ctx.send("Amount must be positive!")
            return
        balance = self.get_balance(user_id)
        if balance < amount:
            await ctx.send("You don't have enough coins!")
        else:
            self.subtract_balance(user_id, amount)
            embed = nextcord.Embed(title="Spent Coins", description=f"You spent {amount} coins.", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command(name="apply", description="Apply for a job")
    async def apply(self, ctx, job_name: str):
        user_id = ctx.author.id
        job_name = job_name.title()

        if job_name not in self.jobs:
            await ctx.send("That job does not exist. Use `.joblist` to see available jobs.")
            return

        current_time = datetime.utcnow()
        last_applied_time = self.job_application_times.get(user_id)

        if last_applied_time is not None and current_time - last_applied_time < timedelta(days=5):
            remaining_time = timedelta(days=5) - (current_time - last_applied_time)
            days, remainder = divmod(remaining_time.seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(f"You can apply for a new job again in {days} days, {hours} hours, and {minutes} minutes.")
            return

        self.user_jobs[user_id] = job_name
        self.job_application_times[user_id] = current_time
        embed = nextcord.Embed(title="Job Application", description=f"You have successfully applied for the {job_name} job!", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="joblist", description="List available jobs")
    async def joblist(self, ctx):
        job_list = "\n".join([f"{job}: {earnings} coins" for job, earnings in self.jobs.items()])
        embed = nextcord.Embed(title="Available Jobs", description=job_list, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="job", description="Do a job to earn money")
    @cooldown(1, 7200, BucketType.user)  # 1 use per 7200 seconds (2 hours) per user
    async def job(self, ctx):
      user_id = ctx.author.id
      job_name = self.user_jobs.get(user_id)
      if job_name:
        earnings = self.jobs[job_name]
        self.add_balance(user_id, earnings)
        embed = nextcord.Embed(title="Job Completed", description=f"You worked as a {job_name} and earned {earnings} coins!", color=0x00ff00)
        await ctx.send(embed=embed)
      else:
        await ctx.send("You have not applied for any job. Use `.apply <job>` to apply for a job.")

    @commands.command(name="rob", description="Rob another user")
    async def rob(self, ctx, member: nextcord.Member):
        if member == ctx.author:
            await ctx.send("You cannot rob yourself!")
            return

        user_id = ctx.author.id
        target_id = member.id

        if self.get_balance(target_id) == 0:
            await ctx.send("The user you are trying to rob has no coins!")
            return

        success_chance = random.randint(1, 100)
        if success_chance > 50:
            amount_stolen = random.randint(1, self.get_balance(target_id))
            self.subtract_balance(target_id, amount_stolen)
            self.add_balance(user_id, amount_stolen)
            embed = nextcord.Embed(title="Robbery Successful", description=f"You successfully robbed {amount_stolen} coins from {member.mention}!", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            penalty = random.randint(1, 50)
            self.subtract_balance(user_id, penalty)
            embed = nextcord.Embed(title="Robbery Failed", description=f"You failed to rob {member.mention} and lost {penalty} coins in the process.", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name="dailystreak", description="Claim your daily reward")
    async def dailystreak(self, ctx):
        user_id = ctx.author.id
        current_time = datetime.utcnow()
        last_claim_time = self.last_claimed.get(user_id)

        if last_claim_time is not None and current_time - last_claim_time < timedelta(hours=24):
            remaining_time = timedelta(hours=24) - (current_time - last_claim_time)
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(f"You can claim your daily reward again in {hours} hours, {minutes} minutes.")
            return

        streak = self.daily_streaks.get(user_id, 0) + 1
        self.daily_streaks[user_id] = streak
        self.last_claimed[user_id] = current_time
        reward = 100 + (streak * 10)  # Base reward of 100 coins + 10 coins for each consecutive day
        self.add_balance(user_id, reward)

        embed = nextcord.Embed(title="Daily Streak Reward", description=f"You have claimed your daily reward and received {reward} coins!\nCurrent streak: {streak} days.", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="shop", description="Display the shop")
    async def shop(self, ctx):
        shop_list = "\n".join([f"{item}: {price} coins" for item, price in self.shop_items.items()])
        embed = nextcord.Embed(title="Shop", description=shop_list, color=0x00ff00)
        await ctx.send(embed=embed)

@commands.command(name="buy", description="Buy an item from the shop")
async def buy(self, ctx, item_name: str):
    user_id = ctx.author.id
    item_name = item_name.title()

    if item_name not in self.shop_items:
        await ctx.send("That item does not exist in the shop.")
        return

    item_price = self.shop_items[item_name]
    if self.get_balance(user_id) < item_price:
        await ctx.send("You don't have enough coins to buy this item.")
        return

    self.subtract_balance(user_id, item_price)
    self.add_item(user_id, item_name)
    await ctx.send(f"You bought {item_name} for {item_price} coins!")

def setup(bot):
    bot.add_cog(Economy(bot))
