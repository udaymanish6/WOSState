from PIL import Image, ImageDraw
from io import BytesIO
import discord
from discord.ext import commands
import requests


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.system_channel
        if welcome_channel:
            welcome_message = f"Welcome to **{member.guild.name}**, {member.mention}!"

            bg_image = Image.new('RGBA', (800, 400), (10, 11, 22))

            avatar_url = str(member.display_avatar.url)
            avatar_response = requests.get(avatar_url)
            avatar_image = Image.open(BytesIO(avatar_response.content)).convert("RGBA")
            avatar_size = 256
            avatar_image = avatar_image.resize((avatar_size, avatar_size))

            mask_im = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask_im)
            mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

            avatar_x = (bg_image.width - avatar_size) // 2
            avatar_y = (bg_image.height - avatar_size) // 2
            bg_image.paste(avatar_image, (avatar_x, avatar_y), mask_im)

            final_buffer = BytesIO()
            bg_image.save(final_buffer, "PNG")
            final_buffer.seek(0)

            file = discord.File(final_buffer, "welcome_image.png")
            await welcome_channel.send(content=welcome_message, file=file)
        else:
            print("System channel not found. Welcome message not sent.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_channel = member.guild.system_channel
        if leave_channel:
            farewell_message = f"Goodbye, **{member.display_name}**. We'll miss you!"

            bg_image = Image.new('RGBA', (800, 400), (10, 11, 22))

            avatar_url = str(member.display_avatar.url)
            avatar_response = requests.get(avatar_url)
            avatar_image = Image.open(BytesIO(avatar_response.content)).convert("RGBA")
            avatar_size = 256
            avatar_image = avatar_image.resize((avatar_size, avatar_size))

            mask_im = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask_im)
            mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

            avatar_x = (bg_image.width - avatar_size) // 2
            avatar_y = (bg_image.height - avatar_size) // 2
            bg_image.paste(avatar_image, (avatar_x, avatar_y), mask_im)

            final_buffer = BytesIO()
            bg_image.save(final_buffer, "PNG")
            final_buffer.seek(0)

            file = discord.File(final_buffer, "farewell_image.png")
            await leave_channel.send(content=farewell_message, file=file)
        else:
            print("Leave channel not found. Farewell message not sent.")


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
