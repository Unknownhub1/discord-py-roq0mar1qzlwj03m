import re
import requests
import discord
import time
import asyncio
token = "[TOKEN]" #봇 토큰번호
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    while True:
        await client.change_presence(activity=discord.Game("!명령어"),status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game("솔로랭크 & 파티랭크 조회 봇"),status=discord.Status.online)
        await asyncio.sleep(3)
        await client.change_presence(activity=discord.Game("비모#9999"),status=discord.Status.online)
        await asyncio.sleep(3)

@client.event
async def on_message(message):
    if message.content.startswith("!청소 "):
        purge_number = message.content.replace("!청소 ", "")
        check_purge_number = purge_number.isdigit()

        if check_purge_number == True:
            await message.channel.purge(limit=int(purge_number) + 1)
            msg = await message.channel.send(f"**{purge_number}개**의 메시지를 삭제했습니다.")
            await asyncio.sleep(1.5)
            await msg.delete()

        else:
            await message.channel.send("올바른 값을 입력해주세요.")
    if message.content == "!명령어":
        embed = discord.Embed(title="INFO BOT", description=f"!솔로 : 닉네임을 통해 솔로랭크 정보 를 확인합니다.\n┗ !솔로 닉네임\n\n!파티 : 닉네임을 통해 파티랭크 정보 를 확인합니다.\n┗ !파티 닉네임\n\n!청소 : 대화 목록을 지워줍니다.\n┗ !청소 숫자 \n\n오류문의: 비모#9999", color=0xB2EBF4)
         
        await message.channel.send(embed=embed)
    
    if message.content.startswith('!솔로 '):
        nickname = message.content.split(" ")[1]
        usernumber = requests.post(f"https://barracks.sa.nexon.com/api/Search/GetSearch/{nickname}/1").json()
        
        try:
            usernumber = usernumber['result']['characterInfo'][0]["user_nexon_sn"]

        except:
            embed = discord.Embed(title="INFO BOT", description="해당 유저를 찾지 못했습니다.", color=0xB2EBF4)
             
            await message.channel.send(embed=embed)
            return
            
        res = requests.post(f"https://barracks.sa.nexon.com/api/GameRecord/GetSeasonUserRankInfo/{str(usernumber)}/2210/RANK_S").json()
        #https://barracks.sa.nexon.com/api/GameRecord/GetSeasonUserRankInfo/1091038190/2208/RANK
        resa = requests.post(f"https://barracks.sa.nexon.com/api/Profile/GetProfileMain/{str(usernumber)}").json()
        ban = resa['result']['characterInfo']['punish_type']

        if ban == 'restriction':
            punish = '운영 정책 위반'

        elif ban == 'protection':
            punish = '보호 모드'
            
        else:
            punish = '-'

        playtime = int(res['rankMatchRecordInfo']["y_rank_play_time"])
        sexunji = res['rankMatchRecordInfo']['y_rank_combine_combat_cnt']
        sexunji2 = res['rankMatchRecordInfo']['y_rank_combine_combat_win']
        dmg = res['rankMatchRecordInfo']["y_rank_combine_damage_avg"]
        ss1 = res['rankMatchRecordInfo']['y_rank_combine_combat_rate']
        ss2 = res['rankMatchRecordInfo']['y_rank_combine_kill_rate']
        rankrp = res['rankMatchRecordInfo']['y_rank_rp_gain']
        rankname = res['rankMatchRecordInfo']['y_rank_class_name']
        ranktier = res['rankMatchRecordInfo']['y_rank_class_image']
        rank = res['rankMatchRecordInfo']['y_rank_rank']
        clanname = "-"
        try:
            clanname = str(resa['result']['characterInfo']["clan_name"])
            if clanname == "":
                clanname = "-"
        except:
            clanname = "-"

        try:
            playtime_sex = round(round(playtime / 60) / int(sexunji), 2)
            minute = str(playtime_sex).split('.')[0]
            second = str(playtime_sex).split('.')[1]
            zin = minute + '분 ' + str(round(int(second) * 0.6)) + "초"
            playtime_sex = round((playtime / 60) / 60, 2)
            hour = str(playtime_sex).split('.')[0]
            minute = str(playtime_sex).split('.')[1]
            total_playtime = hour + '시간 ' + str(round(int(minute) * 0.6)) + "분"
    
            embed = discord.Embed(title=f"**{nickname}**", url=f"https://barracks.sa.nexon.com/{str(usernumber)}/match/", description=f" {rankname} \n {rankrp} RP\n\n", color=0xB2EBF4)
            embed.set_author(name="22년 05특별 부스트업(솔로)")
            embed.add_field(name="클랜", value=f"{clanname} ", inline=False)
            embed.add_field(name="랭킹", value=f"{rank} 위", inline=False)
            embed.add_field(name="상세정보", value=f" 전적 : {sexunji}전 {sexunji2}승\n 승률 : {ss1}%\n 킬데스 : {ss2}%\n 데미지(평균) : {dmg}", inline=False)
            embed.add_field(name="플레이타임", value=f"전체 : {total_playtime}\n평균 : {zin}", inline=False)
            embed.add_field(name="제재현황", value=f"   {punish}", inline=False)
            embed.set_thumbnail(url=f"{ranktier}")   
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="INFO BOT", description=f"**{nickname}** 님은 22년 05특별 부스트업(솔로) 기록이 없습니다.", color=0xB2EBF4)
            await message.channel.send(embed=embed)

    if message.content.startswith('!파티 '):
        nickname = message.content.split(" ")[1]
        usernumber = requests.post(f"https://barracks.sa.nexon.com/api/Search/GetSearch/{nickname}/1").json()
        
        try:
            usernumber = usernumber['result']['characterInfo'][0]["user_nexon_sn"]

        except:
            embed = discord.Embed(title="INFO BOT", description="해당 유저를 찾지 못했습니다.", color=0xB2EBF4)
             
            await message.channel.send(embed=embed)
            return
            
        res = requests.post(f"https://barracks.sa.nexon.com/api/GameRecord/GetSeasonUserRankInfo/{str(usernumber)}/2210/RANK").json()
        #https://barracks.sa.nexon.com/api/GameRecord/GetSeasonUserRankInfo/1091038190/2208/RANK
        resa = requests.post(f"https://barracks.sa.nexon.com/api/Profile/GetProfileMain/{str(usernumber)}").json()
        ban = resa['result']['characterInfo']['punish_type']

        if ban == 'restriction':
            punish = '운영 정책 위반'

        elif ban == 'protection':
            punish = '보호 모드'
            
        else:
            punish = '-'

        playtime = int(res['rankMatchRecordInfo']["y_rank_play_time"])
        sexunji = res['rankMatchRecordInfo']['y_rank_combine_combat_cnt']
        sexunji2 = res['rankMatchRecordInfo']['y_rank_combine_combat_win']
        dmg = res['rankMatchRecordInfo']["y_rank_combine_damage_avg"]
        ss1 = res['rankMatchRecordInfo']['y_rank_combine_combat_rate']
        ss2 = res['rankMatchRecordInfo']['y_rank_combine_kill_rate']
        rankrp = res['rankMatchRecordInfo']['y_rank_rp_gain']
        rankname = res['rankMatchRecordInfo']['y_rank_class_name']
        ranktier = res['rankMatchRecordInfo']['y_rank_class_image']
        rank = res['rankMatchRecordInfo']['y_rank_rank']
        clanname = "-"
        try:
            clanname = str(resa['result']['characterInfo']["clan_name"])
            if clanname == "":
                clanname = "-"
        except:
            clanname = "-"

        try:
            
            playtime_sex = round(round(playtime / 60) / int(sexunji), 2)
            minute = str(playtime_sex).split('.')[0]
            second = str(playtime_sex).split('.')[1]
            zin = minute + '분 ' + str(round(int(second) * 0.6)) + "초"
            playtime_sex = round((playtime / 60) / 60, 2)
            hour = str(playtime_sex).split('.')[0]
            minute = str(playtime_sex).split('.')[1]
            total_playtime = hour + '시간 ' + str(round(int(minute) * 0.6)) + "분"
    

            embed = discord.Embed(title=f"**{nickname}**", url=f"https://barracks.sa.nexon.com/{str(usernumber)}/match/", description=f" {rankname} \n {rankrp} RP\n\n", color=0xB2EBF4)
            embed.set_author(name="22년 05특별 부스트업(파티)")
            embed.add_field(name="클랜", value=f"{clanname} ", inline=False)
            embed.add_field(name="랭킹", value=f"{rank} 위", inline=False)
            embed.add_field(name="상세정보", value=f" 전적 : {sexunji}전 {sexunji2}승\n 승률 : {ss1}%\n 킬데스 : {ss2}%\n 데미지(평균) : {dmg}", inline=False)
            embed.add_field(name="플레이타임", value=f"전체 : {total_playtime}\n평균 : {zin}", inline=False)
            embed.add_field(name="제재현황", value=f"   {punish}", inline=False)
            embed.set_thumbnail(url=f"{ranktier}")   
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="INFO BOT", description=f"**{nickname}** 님은 22년 05특별 부스트업(파티) 기록이 없습니다.", color=0xB2EBF4)
            await message.channel.send(embed=embed)

client.run(token)
