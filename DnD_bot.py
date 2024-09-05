import discord
import random
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

TOKEN = 'YOUR_BOT_TOKEN'
intent = discord.Intents.default()
intent.message_content = True
intent.messages = True
intent.members = True

bot = commands.Bot(command_prefix='!', intents=intent)

def roll(num, r):
    list = []
    for i in range(r):
        list.append(random.randint(1, num))
    list.append(sum(list))
    return list
def roll_str(list, r):
    string = ''
    for i in range(r):
        string += f'{list[i]}, '
    return string.removesuffix(', ')

@bot.command(aliases=['rollstat', 'rollstats', 'Rollstat', 'Rollstats'])
async def rollstats_(ctx):
    list = [[],
            [],
            [],
            [],
            [],
            [],]
    for i in range(6):
        minnum = 0
        for _ in range(4):
            list[i].append(random.randint(1, 6))
        for num in range(4):
            if list[i][num] < list[i][minnum]:
                minnum = num
        list[i][minnum] = f'**{list[i][minnum]}**'
    for i in list:
        summ = 0
        for _ in i:
            if isinstance(_, int):
                summ += _
        i.append(summ)
    await ctx.send(f'''{ctx.author.mention} использовал !rollstats
## Рандомные характеристики:
>>> Характеристика 1: ({roll_str(list[0], 4)}) = {list[0][-1]}
Характеристика 2: ({roll_str(list[1], 4)}) = {list[1][-1]}
Характеристика 3: ({roll_str(list[2], 4)}) = {list[2][-1]}
Характеристика 4: ({roll_str(list[3], 4)}) = {list[3][-1]}
Характеристика 5: ({roll_str(list[4], 4)}) = {list[4][-1]}
Характеристика 6: ({roll_str(list[5], 4)}) = {list[5][-1]}
Суммма всех характеристик: **{list[0][-1]+list[1][-1]+list[2][-1]+list[3][-1]+list[4][-1]+list[5][-1]}**''')

@bot.command(aliases=['r', 'R', 'roll', 'Roll'])
async def r_(ctx, *, string: str):
    try:
        math_string=''
        math_list = []
        last_i = 0
        count_list = []
        for i in range(len(string)):
            if string[i] == '+' or string[i] == '-' or string[i] == '*' or string[i] == '/':
                math_list.append(string[last_i:i])
                math_list.append(string[i])
                last_i = i+1
            if i == len(string)-1:
                math_list.append(string[last_i:])
        for i in math_list:
            count = False
            dice = ''
            for _ in range(len(i)):
                if count:
                    dice += i[_]
                if i[_] == 'd':
                    r = ''
                    count = True
                    for z in range(_):
                        if i[_-z-1].isdigit():
                            r += i[_-z-1]
                        else:
                            math_string += i[:_-z+1]
                            break
            if count:
                roll_list = roll(int(dice), int(r[::-1]))
                math_string += str(roll_list[-1])
                count_list.append(roll_list)
            else:
                math_string += i
                count_list.append([0])
        the_string = ''
        for i in range(len(math_list)):
            x = roll_str(count_list[i], len(count_list[i])-1)
            if x != '':
                x = f'({x})'
            the_string += math_list[i]+x
        final_string = the_string+' = ' + str(eval(math_string))
        if len(final_string) > 2000:
            with open('roll.txt', 'w') as f:
                f.write(final_string)
            file = discord.File('./roll.txt', filename='roll.txt')
            await ctx.send(file=file)
        else: await ctx.send(final_string)
    except: await ctx.send('Ошибка: такие числа невозможно посчитать')

@bot.command(aliases=['bestiary', 'Bestiary', 'b', 'B'])
async def b_(ctx, *, url: str):
    url = f'https://dnd.su/bestiary/?search={url}'

    response = requests.get(url)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('a', {'class': 'item-link'}).get_text()+ '\n'

        size = soup.find('li', {'class': 'size-type-alignment'}).get_text()+ '\n'

        first_mob = soup.find('div', {'class': 'cards-wrapper'})

        li = first_mob.findAll('li')

        armor = ''
        hp = ''
        speed = ''
        stats = soup.findAll('li', {'class': 'abilities'})
        roll_stats = ''
        abilities = ''
        languages = ''
        race_skill = ''
        danger = ''
        master_bonus = ''
        damage_immune = ''
        debuff_immune = ''
        lives = ''
        link = ''
        information = []
        for i in range(len(li)):
            try:
                if li[i]['class'] == ['subsection', 'desc']:
                    information.append(li[i])
                if 'Класс Доспеха' in li[i].get_text():
                    armor = li[i].get_text() + '\n'
                if 'Хиты' in li[i].get_text():
                    hp = li[i].get_text() + '\n'
                if 'Скорость' in li[i].get_text():
                    speed = li[i].get_text() + '\n'
                if 'Языки' in li[i].get_text():
                    languages = li[i].get_text() + '\n'
                if 'Спасброски' in li[i].get_text():
                    roll_stats = li[i].get_text() + '\n'
                if 'Навыки' in li[i].get_text():
                    abilities = li[i].get_text() + '\n'
                if 'Чувства' in li[i].get_text():
                    race_skill = li[i].get_text() + '\n'
                if 'Опасность' in li[i].get_text():
                    danger = li[i].get_text() + '\n'
                if 'Бонус мастерства' in li[i].get_text():
                    master_bonus = li[i].get_text() + '\n'
                if 'Иммунитет к урону' in li[i].get_text():
                    damage_immune = li[i].get_text() + '\n'
                if 'Иммунитет к состоянию' in li[i].get_text():
                    debuff_immune = li[i].get_text() + '\n'
                if 'Местность обитания' in li[i].get_text():
                    lives = li[i].get_text() + '\n'
            except: pass
            if 'Источник' in li[i].get_text():
                link = li[i].get_text() + '\n'
    except: await ctx.send('Ошибка: таких мобов нет в базе')
    final_string = name+size+armor+hp+speed+stats[0].get_text()+'\n'+roll_stats+abilities+damage_immune+debuff_immune+race_skill+languages+danger+master_bonus+lives+link+''.join(map(str, [inf.get_text() for inf in information])).replace('Описание', 'Описание: ').replace('Действия', 'Действия: ')
    if len(final_string) > 2000:
        with open('roll.txt', 'w') as f:
            f.write(final_string)
        file = discord.File('./roll.txt', filename='roll.txt')
        await ctx.send(file=file)
    else: await ctx.send(final_string)

@bot.command(aliases=['item', 'Item', 'i', 'I'])
async def i_(ctx, *, url: str):
    url = f'https://dnd.su/items/?search={url}'

    response = requests.get(url)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        first_mob = soup.find('div', {'class': 'cards-wrapper'})

        name = first_mob.find('a', {'class': 'item-link'}).get_text()+ '\n'

        size = first_mob.find('li', {'class': 'size-type-alignment'}).get_text()+ '\n'

        price = ''

        link = ''

        li = first_mob.findAll('li')

        information = []
        for i in range(len(li)):
            try:
                if li[i]['class'] == ['subsection', 'desc']:
                    information.append(li[i])
                if li[i]['class'] == ['price']:
                    price = li[i].get_text() + '\n'
            except: pass
            if 'Источник' in li[i].get_text():
                link = li[i].get_text() + '\n'
    except: await ctx.send('Ошибка: таких предметов нет в базе')
    final_string = name+size+price+link+''.join(map(str, [inf.get_text() for inf in information]))
    if len(final_string) > 2000:
        with open('roll.txt', 'w') as f:
            f.write(final_string)
        file = discord.File('./roll.txt', filename='roll.txt')
        await ctx.send(file=file)
    else: await ctx.send(final_string)
@bot.command(aliases=['spell', 'Spell', 's', 'S'])
async def s_(ctx, *, url: str):
    url = f'https://dnd.su/spells/?search={url}'

    response = requests.get(url)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        first_mob = soup.find('div', {'class': 'cards-wrapper'})

        name = first_mob.find('a', {'class': 'item-link'}).get_text()+ '\n'

        size = first_mob.find('li', {'class': 'size-type-alignment'}).get_text()+ '\n'

        cast_time = ''
        distance = ''
        components = ''
        duration = ''
        classes = ''
        child_classes = ''
        link = ''

        li = first_mob.findAll('li')

        information = []
        for i in range(len(li)):
            try:
                if li[i]['class'] == ['subsection', 'desc']:
                    information.append(li[i])
            except: pass
            if 'Источник' in li[i].get_text():
                link = li[i].get_text() + '\n'
            if 'Время накладывания:' in li[i].get_text():
                cast_time = li[i].get_text() + '\n'
            if 'Дистанция:' in li[i].get_text():
                distance = li[i].get_text() + '\n'
            if 'Компоненты:' in li[i].get_text():
                components = li[i].get_text() + '\n'
            if 'Длительность:' in li[i].get_text():
                duration = li[i].get_text() + '\n'
            if 'Классы:' in li[i].get_text():
                classes = li[i].get_text() + '\n'
            if 'Подклассы:' in li[i].get_text():
                child_classes = li[i].get_text() + '\n'
    except: await ctx.send('Ошибка: таких заклинаний нет в базе')
    final_string = name+size+cast_time+distance+components+duration+classes+child_classes+link+''.join(map(str, [inf.get_text() for inf in information]))
    if len(final_string) > 2000:
        with open('roll.txt', 'w') as f:
            f.write(final_string)
        file = discord.File('./roll.txt', filename='roll.txt')
        await ctx.send(file=file)
    else: await ctx.send(final_string)

bot.run(TOKEN)