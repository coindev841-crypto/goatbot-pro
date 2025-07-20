import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logado como {bot.user}")

@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="geral")
    if canal:
        await canal.send(f"👋 Bem-vindo(a) {member.mention}!")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int = 5):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"🧹 {quantidade} mensagens limpas.", delete_after=5)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Motivo não especificado"):
    await membro.ban(reason=motivo)
    await ctx.send(f"🔨 {membro.mention} foi banido.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo="Motivo não especificado"):
    await membro.kick(reason=motivo)
    await ctx.send(f"👢 {membro.mention} foi expulso.")

@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    await ctx.send(membro.avatar.url)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=guild.name, description="Informações do servidor", color=0x00ff00)
    embed.add_field(name="Dono", value=guild.owner, inline=True)
    embed.add_field(name="Membros", value=guild.member_count, inline=True)
    embed.add_field(name="Canais", value=len(guild.channels), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    embed = discord.Embed(title="Informações do Usuário", color=0x00ff00)
    embed.set_thumbnail(url=membro.avatar.url)
    embed.add_field(name="Nome", value=membro.name)
    embed.add_field(name="ID", value=membro.id)
    embed.add_field(name="Entrou em", value=membro.joined_at.strftime("%d/%m/%Y"))
    await ctx.send(embed=embed)

@bot.command()
async def diga(ctx, *, mensagem):
    await ctx.send(mensagem)

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="📖 Lista de Comandos", color=0x3498db)
    comandos = {
        "ping": "Verifica a latência do bot.",
        "limpar [n]": "Limpa n mensagens.",
        "ban @membro": "Bane o membro.",
        "kick @membro": "Expulsa o membro.",
        "avatar [@membro]": "Mostra o avatar do usuário.",
        "serverinfo": "Mostra informações do servidor.",
        "userinfo [@membro]": "Mostra informações do usuário.",
        "diga [mensagem]": "Faz o bot repetir uma mensagem.",
    }
    for nome, desc in comandos.items():
        embed.add_field(name=f"!{nome}", value=desc, inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)