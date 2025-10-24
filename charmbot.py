'''
   ____       _    _         __          _____       __    __      ____        ____       _______    
  / __ \     | |  | |      /    \       |  __ \     |  \  /  |    |  _ \      / __ \     |__   __|   
 / /  \_|    | |__| |     /  /\  \      | |__) |    |   \/   |    | |_| |    | |  | |       | |      
| |          |  __  |    /  /__\  \     |  _  /     | |\  /| |    |  _  {    | |  | |       | |      
| \____      | |  | |   /  /    \  \    | | \ \     | | \/ | |    | |_| |    | |__| |       | |      
 \_____|     |_|  |_|   \_/      \_/    |_|  \_\    |_|    |_|    |____/      \____/        |_|   


Copyright (c) 2025 Marcin Filipiak
Licensed under the MIT License.

'''

# ─────────────────────────────────────────────────────────────
# ✅ Importy
# ─────────────────────────────────────────────────────────────
import discord
from discord.ext import commands
import random
from datetime import timedelta
import asyncio 

import io
import aiohttp
from PIL import Image

from config import *

# ─────────────────────────────────────────────────────────────
# 📁 Inicjalizacja Intencji i Bota
# ─────────────────────────────────────────────────────────────
# Intents określają, do jakich zdarzeń i danych bot ma dostęp.
# Domyślnie włączone są tylko podstawowe, więc tu ręcznie aktywujemy potrzebne:
intents = discord.Intents.default()
intents.message_content = True   # pozwala botowi czytać treść wiadomości (konieczne np. do filtrowania i flirtów)
intents.messages = True          # umożliwia reagowanie na nowe i edytowane wiadomości
intents.reactions = True         # pozwala obsługiwać reakcje emoji dodawane do wiadomości
intents.guilds = True            # pozwala botowi widzieć serwery (guilds), ich nazwy i kanały
intents.members = True           # umożliwia dostęp do listy użytkowników i nadawanie ról


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ─────────────────────────────────────────────────────────────
# 📄 Wczytywanie danych z plików
# ─────────────────────────────────────────────────────────────

def load_banned_phrases():
    """Wczytuje listę zakazanych fraz z pliku."""
    with open(BANNED_PHRASES_FILE, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def load_flirty_responses():
    """Wczytuje listę flirtujących odpowiedzi z pliku."""
    try:
        with open(FLIRTY_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Plik {FLIRTY_FILE} nie został znaleziony.")
        return ["Cześć, chcesz pogadać? 😅"]

BANNED_PHRASES = load_banned_phrases()

# ─────────────────────────────────────────────────────────────
# 📢 Stempel do obrazka
# ─────────────────────────────────────────────────────────────

async def add_stamp_to_image(image_url, stamp_path="stamp.gif"):
    """
    Pobiera obraz z URL i nakłada stempelek (logo) w lewym dolnym rogu z 60% przezroczystością.
    Zwraca BytesIO gotowy do wysłania na Discord.
    """
    # Pobranie obrazu z internetu
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status != 200:
                return None
            image_bytes = await resp.read()

    # Otwieramy bazę i stempelek
    base = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    overlay = Image.open(stamp_path).convert("RGBA")

    # Ustawienie przezroczystości nakładki
    alpha = overlay.split()[3]
    alpha = alpha.point(lambda p: p * 0.6)
    overlay.putalpha(alpha)

    # Pozycjonowanie w lewym dolnym rogu
    base_width, base_height = base.size
    overlay_width, overlay_height = overlay.size
    position = (0, base_height - overlay_height)

    # Nakładamy stempelek
    base.paste(overlay, position, overlay)

    # Konwertujemy wynik na RGB (usuwa alfa, miesza z tłem)
    result = base.convert("RGB")

    # Zapis do pamięci
    output = io.BytesIO()
    result.save(output, format="JPEG")
    output.seek(0)
    return output


# ─────────────────────────────────────────────────────────────
# 📢 Eventy Bota
# ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    """Wydarzenie uruchamiane po starcie bota."""
    print(f'Zalogowano jako {bot.user}')
    if ENABLE_TASKS:
        print(f'Zadania cron bota włączone')
        bot.loop.create_task(periodic_bump_reminder())
    else: 
        print(f'Zadania cron bota wyłączone')

@bot.event
async def on_message(message):
    """Obsługa nowej wiadomości — sprawdzanie fraz, przydzielanie roli i flirtowanie."""
    if message.author.bot:
        return
        
    content_lower = message.content.lower()

    # Sprawdź zakazane frazy
    if any(phrase in content_lower for phrase in BANNED_PHRASES):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, dostałeś przerwę. Zapoznaj się z regulaminem.")
        await timeout_member(message.author, TIMEOUT_DURATION_SECONDS, "Naruszenie regulaminu", message)
        return

    await give_role_if_needed(message.author)

    # Flirt tylko jeśli wiadomość nie jest reply do wiadomości bota
    if bot.user in message.mentions:
        is_reply_to_bot = False
        if message.reference:
            try:
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                if replied_message.author.bot:
                    is_reply_to_bot = True
            except Exception:
                pass
        if not is_reply_to_bot:
            flirt = random.choice(load_flirty_responses())
            await message.channel.send(flirt)

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    """Reakcje — sprawdzanie ról."""
    if user.bot:
        return
    guild = reaction.message.guild
    member = guild.get_member(user.id)
    if member:
        await give_role_if_needed(member)
        
        
# ─────────────────────────────────────────────────────────────
# 📢 CRON
# ─────────────────────────────────────────────────────────────        
        
# Zadanie tła do wysyłania przypomnienia o bumpie co określony czas
async def periodic_bump_reminder():
    if BUMP_INTERVAL_HOURS > 0:
            await bot.wait_until_ready()  # Poczekaj aż bot się zaloguje
            while not bot.is_closed():
                for guild in bot.guilds:
                    channel = discord.utils.get(guild.text_channels, name=BUMP_CHANNEL_NAME)
                    if channel:
                        try:
                            await channel.send("🔼 Hej! Nie zapomnij podbić naszego serwera! Wpisz `/bump` 💬")
                        except discord.Forbidden:
                            print(f"Brak uprawnień do pisania na kanale {BUMP_CHANNEL_NAME} w serwerze {guild.name}")
                await asyncio.sleep(BUMP_INTERVAL_HOURS * 3600)

# ─────────────────────────────────────────────────────────────
# 👮‍♂️ Funkcje Moderacyjne
# ─────────────────────────────────────────────────────────────

async def give_role_if_needed(member):
    """Nadaje rolę użytkownikowi, jeśli jej jeszcze nie ma."""
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role and role not in member.roles:
        await member.add_roles(role)
        print(f'Nadano rolę {ROLE_NAME} użytkownikowi {member.name}')

async def timeout_member(member, duration_seconds, reason, original_message):
    """Nakłada timeout na użytkownika i wysyła informację na kanał moderatorów."""
    try:
        until = discord.utils.utcnow() + timedelta(seconds=duration_seconds)
        await member.timeout(until, reason=reason)
        print(f"{member.name} został wyciszony.")

        mod_channel = discord.utils.get(member.guild.text_channels, name=MOD_CHANNEL_NAME)
        if mod_channel:
            embed = discord.Embed(title="⛔ Timeout nałożony", color=discord.Color.red())
            embed.add_field(name="Użytkownik", value=member.mention, inline=True)
            embed.add_field(name="Czas trwania", value="24 godziny", inline=True)
            embed.add_field(name="Powód", value=reason, inline=False)
            embed.add_field(name="Treść wiadomości", value=original_message.content, inline=False)
            embed.set_footer(text=f"ID: {member.id}")
            await mod_channel.send(embed=embed)
    except Exception as e:
        print(f"Nie udało się nałożyć timeoutu: {e}")

# ─────────────────────────────────────────────────────────────
# 🧩 Komendy Bota
# ─────────────────────────────────────────────────────────────

@bot.command()
async def ping(ctx):
    """Testowa komenda sprawdzająca responsywność."""
    await ctx.send("Pong!")

@bot.command()
async def zaczep(ctx, *, channel_name: str):
    """
    Wysyła zaczepkę do losowego użytkownika,
    który ostatnio zareagował na wiadomość w danym kanale.
    """
    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
    if not channel:
        await ctx.send("Nie znaleziono takiego kanału.")
        return

    last_reacted_users = set()

    async for message in channel.history(limit=20):
        for reaction in message.reactions:
            async for user in reaction.users():
                if not user.bot:
                    last_reacted_users.add(user)

    if not last_reacted_users:
        await ctx.send("Brak reakcji na ostatnie wiadomości.")
        return

    random_user = random.choice(list(last_reacted_users))
    flirt = random.choice(load_flirty_responses())

    try:
        await channel.send(f"{random_user.mention}, {flirt}")
        await ctx.send(f"Zaczepka wysłana do {random_user.mention} na kanał **{channel.name}**.")
    except discord.Forbidden:
        await ctx.send("Nie mam uprawnień do pisania na tym kanale.")


@bot.command()
@commands.has_permissions(administrator=True)
async def stamp(ctx, *, text_after_command: str = ""):
    """Nakłada stempel na załączone obrazki."""
    files_to_send = []

    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                stamped_image = await add_stamp_to_image(attachment.url)
                if stamped_image:
                    files_to_send.append(discord.File(stamped_image, filename=f"stamped_{attachment.filename}"))

    # Usuń wiadomość z komendą
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        print(f"Brak uprawnień do usunięcia wiadomości użytkownika {ctx.author} na kanale {ctx.channel.name}")
    except discord.HTTPException as e:
        print(f"Błąd przy usuwaniu wiadomości: {e}")

    # Wyślij wynik
    if text_after_command or files_to_send:
        await ctx.send(content=text_after_command, files=files_to_send)


# ─────────────────────────────────────────────────────────────
# ▶️ Start Bota
# ─────────────────────────────────────────────────────────────
bot.run(TOKEN)

