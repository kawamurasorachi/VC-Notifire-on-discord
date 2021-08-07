import os,discord
from dotenv import load_dotenv
import re

load_dotenv(override=True)

client = discord.Client(intents=discord.Intents.all())
vcn_channel = {}

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('VC通知をするチャンネルに/vcn_hereと入力してください。')
        break
    for guild in client.guilds:
        print(guild.name)

@client.event
async def on_guild_remove(guild):
    if f'{guild.id}' in vcn_channel.keys():
        vcn_channel.pop(f'{guild.id}')
    print(vcn_channel)

@client.event
async def on_message(message):
    if len(message.content) >= 9:
        if message.content[:9] == '/vcn_help':
            await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                    "/vcn_invite ： 招待リンクを表示 \n" +
                                    "/vcn_here ： VC入室ログチャンネルをこのコマンドが送信されたチャンネルに設定します。")
        if message.content[:9] == '/vcn_invite':
            await message.channel.send("招待リンク：\n"+"https://discord.com/api/oauth2/authorize?client_id=869553096861294602&permissions=2181056512&scope=bot")
        if message.content[:9] == '/vcn_here':
            vcn_channel[f'{message.guild.id}'] = message.channel.id
            await message.channel.send(f"VC入室ログチャンネルをここに設定します。")
    print(vcn_channel)

@client.event
async def on_voice_state_update(member, before, after):
    if f'{member.guild.id}' in vcn_channel.keys():
        alert_channel = client.get_channel(vcn_channel[f'{member.guild.id}'])
        if before.channel is None:
            embed = discord.Embed(
                title=f"{member.nick or member.name}が {after.channel.name} に参加しました", description="こんちゃ", color=0xff0000)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)
        elif after.channel is None:
            embed = discord.Embed(
                title=f"{member.nick or member.name}が {before.channel.name} から抜けました", description="お疲れ", color=0xff0000,)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)

client.run(os.environ.get("DISCORD_TOKEN"))