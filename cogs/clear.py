import discord
from discord.ext import commands
from discord import app_commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Clears a specified number of messages in the channel.")
    @app_commands.describe(number="Number of messages to delete (1-100)")
    async def clear(self, interaction: discord.Interaction, number: app_commands.Range[int, 1, 100]):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=number)
        await interaction.followup.send(f"Deleted {len(deleted)} message(s).", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
