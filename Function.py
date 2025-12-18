import discum
import json
import time
import requests
import Vars
from datetime import datetime
from discum.utils.slash import SlashCommander
from i18n import get_text

try:
    from icecream import ic
except ImportError:
    ic = lambda *args: print(*args) if args else None

botID = '432610292342587392' 
auth = {'authorization' : Vars.token}
bot = discum.Client(token = Vars.token, log=False)
url = (f'https://discord.com/api/v8/channels/{Vars.channelId}/messages')
myUserID = Vars.userId
emoji = '✅'

def checkUserStatus():
    import re
    lang = Vars.language
    print(get_text('log_checking_status', lang))
    requests.post(url=url, headers=auth, data={'content': '$tu'})
    time.sleep(2)
    
    r = requests.get(url, headers=auth)
    jsonResponse = json.loads(r.text)
    
    userInfo = {
        'canMarryNow': False,
        'timeUntilMarry': None,
        'rollsRemaining': 0,
        'timeInMinutes': None,
        'timeUntilReset': None,
        'canGetDk': False
    }
    
    botResponse = None
    if jsonResponse and len(jsonResponse) > 0:
        for message in jsonResponse:
            if message.get('author', {}).get('id') == botID:
                botResponse = message
                break
    
    if botResponse:
        content = botResponse.get('content', '')
        ic(content)
        
        if get_text('check_can_marry', lang) in content:
            userInfo['canMarryNow'] = True
            
            nextResetMatch = re.search(get_text('check_next_reset', lang), content)
            if nextResetMatch:
                timeStr = nextResetMatch.group(1)
                userInfo['timeUntilMarry'] = timeStr + 'min'
                
                timeMatch = re.search(r'(\d+)h (\d+)', timeStr)
                if timeMatch:
                    hours = int(timeMatch.group(1))
                    minutes = int(timeMatch.group(2))
                    userInfo['timeUntilReset'] = hours * 60 + minutes
                else:
                    minutesOnly = re.search(r'(\d+)', timeStr)
                    if minutesOnly:
                        userInfo['timeUntilReset'] = int(minutesOnly.group(1))
            else:
                userInfo['timeUntilMarry'] = '0min'
                userInfo['timeUntilReset'] = 0
            userInfo['timeInMinutes'] = 0
        else:
            marryMatch = re.search(get_text('check_marry_cooldown', lang), content)
            if marryMatch:
                timeStr = marryMatch.group(1)
                userInfo['timeUntilMarry'] = timeStr + 'min'
                
                timeMatch = re.search(r'(\d+)h (\d+)', timeStr)
                if timeMatch:
                    hours = int(timeMatch.group(1))
                    minutes = int(timeMatch.group(2))
                    userInfo['timeInMinutes'] = hours * 60 + minutes
                else:
                    minutesOnly = re.search(r'(\d+)', timeStr)
                    if minutesOnly:
                        userInfo['timeInMinutes'] = int(minutesOnly.group(1))
        
        rollsMatch = re.search(get_text('check_rolls_remaining', lang), content)
        if rollsMatch:
            userInfo['rollsRemaining'] = int(rollsMatch.group(1))
        
        if get_text('check_dk_ready', lang) in content:
            userInfo['canGetDk'] = True
        elif get_text('check_dk_cooldown', lang) in content:
            userInfo['canGetDk'] = False
    
    print('='*50)
    print(f'{get_text("log_can_marry_now", lang)}: {userInfo["canMarryNow"]}')
    print(f'{get_text("log_time_until_marry", lang)}: {userInfo["timeUntilMarry"]}')
    print(f'{get_text("log_rolls_remaining", lang)}: {userInfo["rollsRemaining"]}')
    print(f'{get_text("log_dk_available", lang)}: {userInfo["canGetDk"]}')
    print('='*50)
    
    return userInfo

def shouldClaim(cardName, cardSeries, cardPower, isScheduleActive):
    if cardName in Vars.wishlist:
        if Vars.wishlistMode == 'all' or isScheduleActive:
            return True
    if cardSeries in Vars.desiredSeries:
        if Vars.desiredSeriesMode == 'all' or isScheduleActive:
            return True
    if cardPower >= Vars.minCardPower:
        if Vars.minCardPowerMode == 'all' or isScheduleActive:
            return True
    return False

def claimCard(cardName, idMessage):
    lang = Vars.language
    print(f'{get_text("log_trying_claim", lang)} {cardName}')
    response = requests.put(f'https://discord.com/api/v8/channels/{Vars.channelId}/messages/{idMessage}/reactions/{emoji}/%40me', headers=auth)
    return response.status_code == 204

def processCard(jsonCard, isScheduleActive, rollUserId=None):
    claimed = '❤️'
    unclaimed = '🤍'
    kakera = '💎'
    
    cardInfo = {
        'name': 'null',
        'series': 'null',
        'power': 0,
        'idMessage': jsonCard['id'],
        'wasClaimed': False,
        'isAlreadyClaimed': False
    }
    
    try:
        cardInfo['name'] = jsonCard['embeds'][0]['author']['name']
        cardInfo['series'] = jsonCard['embeds'][0]['description'].replace('\n', '**').split('**')[0]
        cardInfo['power'] = int(jsonCard['embeds'][0]['description'].split('**')[1])
    except (IndexError, KeyError, ValueError):
        pass
    
    if not 'footer' in jsonCard['embeds'][0] or not 'icon_url' in jsonCard['embeds'][0]['footer']:
        lang = Vars.language
        print(unclaimed+' ---- ',cardInfo['power'],' - '+cardInfo['name']+' - '+cardInfo['series'])
        if shouldClaim(cardInfo['name'], cardInfo['series'], cardInfo['power'], isScheduleActive):
            isOwnRoll = isScheduleActive or (rollUserId is not None and rollUserId == myUserID)
            
            if not isOwnRoll:
                print(get_text('log_anti_steal', lang))
                print(get_text('log_waiting_single', lang))
                time.sleep(8)

            time.sleep(2)
            cardInfo['wasClaimed'] = claimCard(cardInfo['name'], cardInfo['idMessage'])
    else:
        cardInfo['isAlreadyClaimed'] = True
        print(claimed+' ---- ',cardInfo['power'],' - '+cardInfo['name']+' - '+cardInfo['series'])
    
    if jsonCard['components'] and len(jsonCard['components']) > 0 and jsonCard['components'][0].get('components'):
        if Vars.desiredKakerasMode == 'all' or isScheduleActive:
            lang = Vars.language
            cardsKakera = jsonCard['components'][0]['components'][0]['emoji']['name']
            components = jsonCard['components'][0]['components']
            for index in range(len(components)):
                try:
                    if cardInfo['isAlreadyClaimed']:
                        print(f'{get_text("log_has_kakera", lang)}: {cardsKakera}')
                    if cardsKakera in Vars.desiredKakeras:
                        print(f'{kakera} - {kakera} - {get_text("log_trying_react_kakera", lang)} {cardsKakera} {get_text("log_kakera_of", lang)} {cardInfo["name"]}')
                        time.sleep(0.5)
                        bot.click(jsonCard['author']['id'], channelID=jsonCard['channel_id'], guildID=Vars.serverId, messageID=jsonCard['id'], messageFlags=jsonCard['flags'], data={'component_type': 2, 'custom_id': components[index]['custom_id']})
                        time.sleep(0.5)
                except IndexError:
                    pass
    
    return cardInfo

def simpleRoll():
    lang = Vars.language
    if Vars.snooze:
        currentHour = datetime.now().hour
        snoozeBegin = int(Vars.snoozeBegin)
        snoozeEnd = int(Vars.snoozeEnd)
        
        if snoozeBegin < snoozeEnd:
            inSnoozeTime = snoozeBegin <= currentHour < snoozeEnd
        else:
            inSnoozeTime = currentHour >= snoozeBegin or currentHour < snoozeEnd
        
        if inSnoozeTime:
            print(get_text('log_snooze_active', lang, hour=currentHour, begin=snoozeBegin, end=snoozeEnd))
            return
    
    print(f'{get_text("log_rolling_at", lang)} {time.strftime("%H:%M - %d/%m/%y", time.localtime())}')
    
    userStatus = checkUserStatus()
    
    if userStatus['rollsRemaining'] == 0:
        print(get_text('log_no_rolls', lang))
        return
    
    if Vars.claimDk and userStatus['canGetDk']:
        print(get_text('log_dk_available_exec', lang))
        requests.post(url=url, headers=auth, data={'content': '$dk'})
        time.sleep(3)
        requests.post(url=url, headers=auth, data={'content': '$daily'})
        print(get_text('log_dk_daily_done', lang))
        time.sleep(2)
    
    canUseMarryFeature = False
    if Vars.marryLastRoll:
        if userStatus['canMarryNow'] and userStatus['timeUntilReset'] is not None and userStatus['timeUntilReset'] < 60:
            canUseMarryFeature = True
            print(get_text('log_marry_active', lang))
            if Vars.divorceLastRoll:
                print(get_text('log_divorce_active', lang))
        else:
            print(get_text('log_marry_inactive', lang, time=userStatus['timeUntilMarry']))
    
    i = 0
    rollCommand = SlashCommander(bot.getSlashCommands(botID).json()).get([Vars.rollCommand])
    cardsRolled = []
    anyClaimed = False
    maxRolls = userStatus['rollsRemaining']
    errorCount = 0
    maxErrors = 3

    while i < maxRolls:
        bot.triggerSlashCommand(botID, Vars.channelId, Vars.serverId, data=rollCommand)
        time.sleep(1.8)
        r = requests.get(url, headers=auth)
        jsonCard = json.loads(r.text)

        if len(jsonCard[0]['content']) != 0:
            errorCount += 1
            print(get_text('log_invalid_message', lang, count=errorCount, max=maxErrors))
            
            if errorCount >= maxErrors:
                print(get_text('log_error_limit', lang))
                break
            
            userStatus = checkUserStatus()
            if userStatus['rollsRemaining'] == 0:
                print(get_text('log_no_rolls_after_check', lang))
                break
            
            maxRolls = i + userStatus['rollsRemaining']
            continue
        
        i += 1
        print(i, ' - ', end='')
        cardInfo = processCard(jsonCard[0], isScheduleActive=True)
        
        if canUseMarryFeature:
            cardsRolled.append(cardInfo)
        
        if cardInfo['wasClaimed']:
            anyClaimed = True
        
    if canUseMarryFeature and not anyClaimed and len(cardsRolled) > 0:
        validCards = [card for card in cardsRolled if not card['isAlreadyClaimed'] and card['name'] != 'null']
        
        if validCards:
            highestPowerCard = max(validCards, key=lambda card: card['power'])
            print(f'\n{get_text("log_applying_marry", lang, name=highestPowerCard["name"], power=highestPowerCard["power"])}')
            claimSuccess = claimCard(highestPowerCard['name'], highestPowerCard['idMessage'])
            
            if claimSuccess and Vars.divorceLastRoll:
                print(get_text('log_divorcing', lang, name=highestPowerCard['name']))
                time.sleep(2)
                requests.post(url=url, headers=auth, data={'content': f'$divorce {highestPowerCard["name"]}'}) 
                time.sleep(2)
                requests.post(url=url, headers=auth, data={'content': 'y'})
                print(get_text('log_divorce_complete', lang))
    
    print(get_text('log_rolling_ended', lang))

    if Vars.pokeRoll:
        print(f'\n{get_text("log_trying_pokeslot", lang)}')
        requests.post(url=url, headers=auth, data={'content': '$p'})

def watchMessages():
    @bot.gateway.command
    def onMessage(resp):
        if resp.event.message:
            message = resp.parsed.auto()
            if message['channel_id'] == Vars.channelId and message['author']['id'] == botID:
                if 'embeds' in message and len(message['embeds']) > 0:
                    try:
                        rollUserId = None
                        if 'interaction' in message and 'user' in message['interaction']:
                            rollUserId = message['interaction']['user']['id']
                        
                        processCard(message, isScheduleActive=False, rollUserId=rollUserId)
                    except Exception as e:
                        pass
    
    bot.gateway.run()
