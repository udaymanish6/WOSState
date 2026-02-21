import discord
from discord.ext import commands

class SupportOperations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_support_menu(self, interaction: discord.Interaction):
        support_menu_embed = discord.Embed(
            title="🆘  Support",
            description=(
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "❄️ **Whiteout Survival Bot** — Help & Info\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "📝  **Request Support** — get help on our Discord\n"
                "ℹ️  **About Project** — open source info & links"
            ),
            color=0x5865F2
        )

        view = SupportView(self)
        
        try:
            await interaction.response.edit_message(embed=support_menu_embed, view=view)
        except discord.errors.InteractionResponded:
            await interaction.message.edit(embed=support_menu_embed, view=view)

    async def show_support_info(self, interaction: discord.Interaction):
        support_embed = discord.Embed(
            title="🤖  Support",
            description=(
                "Need help? Join our community or open an issue on GitHub.\n\n"
                "💬  [Discord Server](https://discord.gg/apYByj6K2m)\n"
                "📦  [GitHub Repository](https://github.com/whiteout-project/bot)\n"
                "🐛  [Report an Issue](https://github.com/whiteout-project/bot/issues)\n\n"
                "Please include as much detail as possible when reporting problems."
            ),
            color=0x5865F2
        )
        
        try:
            await interaction.response.send_message(embed=support_embed, ephemeral=True)
            try:
                await interaction.user.send(embed=support_embed)
            except discord.Forbidden:
                await interaction.followup.send(
                    "❌ Could not send DM because your DMs are closed!",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error sending support info: {e}")

class SupportView(discord.ui.View):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    @discord.ui.button(
        label="Request Support",
        emoji="📝",
        style=discord.ButtonStyle.primary,
        custom_id="request_support"
    )
    async def support_request_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.show_support_info(interaction)

    @discord.ui.button(
        label="About Project",
        emoji="ℹ️",
        style=discord.ButtonStyle.primary,
        custom_id="about_project"
    )
    async def about_project_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        about_embed = discord.Embed(
            title="❄️  Whiteout Survival Bot",
            description=(
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "An open-source Discord bot for **Whiteout Survival**,\n"
                "built and maintained by the **WOSLand** community.\n\n"
                "🏰 **Features**\n"
                "🛡️ Alliance management · 🎁 Gift codes · 👥 Member tracking\n"
                "🐻 Bear trap alerts · 🆔 ID verification · and more\n\n"
                "🔗 **Links**\n"
                "📦  [GitHub](https://github.com/whiteout-project/bot)  ·  "
                "💬  [Discord](https://discord.gg/apYByj6K2m)\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=0x57F287
        )
        about_embed.set_footer(text="❄️ Whiteout Survival Bot")
        
        try:
            await interaction.response.send_message(embed=about_embed, ephemeral=True)
            try:
                await interaction.user.send(embed=about_embed)
            except discord.Forbidden:
                await interaction.followup.send(
                    "❌ Could not send DM because your DMs are closed!",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error sending project info: {e}")

    @discord.ui.button(
        label="Main Menu",
        emoji="🏠",
        style=discord.ButtonStyle.secondary,
        custom_id="main_menu"
    )
    async def main_menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        alliance_cog = self.cog.bot.get_cog("Alliance")
        if alliance_cog:
            try:
                await interaction.message.edit(content=None, embed=None, view=None)
                await alliance_cog.show_main_menu(interaction)
            except discord.errors.InteractionResponded:
                await interaction.message.edit(content=None, embed=None, view=None)
                await alliance_cog.show_main_menu(interaction)

async def setup(bot):
    await bot.add_cog(SupportOperations(bot))