import discum
import json
import time
import requests
import Vars
import base64
from datetime import datetime
from icecream import ic
from discum.utils.slash import SlashCommander

botID = '432610292342587392' 
auth = {'authorization' : Vars.token}
bot = discum.Client(token = Vars.token, log=False)
url = (f'https://discord.com/api/v8/channels/{Vars.channelId}/messages')
emoji = '👍'

try:
    myUserID = json.loads(base64.b64decode(Vars.token.split('.')[0] + '==').decode('utf-8'))['id']
except:
    myUserID = None

def checkUserStatus():
    import re
    print('Verificando status do usuário...')
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
        
        if 'você __pode__ se casar agora mesmo' in content or 'você pode se casar agora mesmo' in content.lower():
            userInfo['canMarryNow'] = True
            
            nextResetMatch = re.search(r'A próxima reinicialização é em \*\*((?:\d+h )?\d+)\*\* min', content)
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
            marryMatch = re.search(r'antes que você possa se casar novamente \*\*((?:\d+h )?\d+)\*\* min', content)
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
        
        rollsMatch = re.search(r'Você tem \*\*(\d+)\*\* rolls restantes', content)
        if rollsMatch:
            userInfo['rollsRemaining'] = int(rollsMatch.group(1))
        
        if '$dk está pronto!' in content:
            userInfo['canGetDk'] = True
        elif 'O próximo $dk em' in content:
            userInfo['canGetDk'] = False
    
    print('='*50)
    print(f'Pode se casar agora: {userInfo["canMarryNow"]}')
    print(f'Tempo até casar: {userInfo["timeUntilMarry"]}')
    print(f'Rolls restantes: {userInfo["rollsRemaining"]}')
    print(f'$dk disponível: {userInfo["canGetDk"]}')
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
    print('Trying to Claim '+ cardName)
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
        print(unclaimed+' ---- ',cardInfo['power'],' - '+cardInfo['name']+' - '+cardInfo['series'])
        if shouldClaim(cardInfo['name'], cardInfo['series'], cardInfo['power'], isScheduleActive):
            isOwnRoll = isScheduleActive or (rollUserId is not None and rollUserId == myUserID)
            
            if not isOwnRoll:
                print(f'Zé povinho aqui não ✋🚫, anti roubo ativado')
                print(f'Esposa(o) de alguém detectada(o). Esperando ficar solteira 😋...')
                time.sleep(10)
            
            cardInfo['wasClaimed'] = claimCard(cardInfo['name'], cardInfo['idMessage'])
    else:
        cardInfo['isAlreadyClaimed'] = True
        print(claimed+' ---- ',cardInfo['power'],' - '+cardInfo['name']+' - '+cardInfo['series'])
    
    if jsonCard['components'] and len(jsonCard['components']) > 0 and jsonCard['components'][0].get('components'):
        if Vars.desiredKakerasMode == 'all' or isScheduleActive:
            cardsKakera = jsonCard['components'][0]['components'][0]['emoji']['name']
            components = jsonCard['components'][0]['components']
            for index in range(len(components)):
                try:
                    if cardsKakera in Vars.desiredKakeras:
                        print(kakera+' - '+kakera+' - Trying to react to '+ cardsKakera+ ' of '+ cardInfo['name'])
                        bot.click(jsonCard['author']['id'], channelID=jsonCard['channel_id'], guildID=Vars.serverId, messageID=jsonCard['id'], messageFlags=jsonCard['flags'], data={'component_type': 2, 'custom_id': components[index]['custom_id']})
                        time.sleep(0.5)
                except IndexError:
                    pass
    
    return cardInfo

def simpleRoll():
    if Vars.snooze:
        currentHour = datetime.now().hour
        snoozeBegin = int(Vars.snoozeBegin)
        snoozeEnd = int(Vars.snoozeEnd)
        
        if snoozeBegin < snoozeEnd:
            inSnoozeTime = snoozeBegin <= currentHour < snoozeEnd
        else:
            inSnoozeTime = currentHour >= snoozeBegin or currentHour < snoozeEnd
        
        if inSnoozeTime:
            print(f'Snooze ativo: {currentHour:02d}h está entre {snoozeBegin:02d}h e {snoozeEnd:02d}h. Ignorando execução.')
            return
    
    print(time.strftime("Rolling at %H:%M - %d/%m/%y", time.localtime()))
    
    userStatus = checkUserStatus()
    
    if userStatus['rollsRemaining'] == 0:
        print('Nenhum roll disponível. Pulando execução.')
        return
    
    if Vars.claimDk and userStatus['canGetDk']:
        print('$dk disponível! Executando claim...')
        requests.post(url=url, headers=auth, data={'content': '$dk'})
        time.sleep(3)
        requests.post(url=url, headers=auth, data={'content': '$daily'})
        print('$dk e $daily executados.')
        time.sleep(2)
    
    canUseMarryFeature = False
    if Vars.marryLastRoll:
        if userStatus['canMarryNow'] and userStatus['timeUntilReset'] is not None and userStatus['timeUntilReset'] < 60:
            canUseMarryFeature = True
            print(f'marryLastRoll: ATIVO - Casará no último roll se nenhum for claimado')
            if Vars.divorceLastRoll:
                print(f'divorceLastRoll: ATIVO - Divorciará após casar')
        else:
            print(f'marryLastRoll: INATIVO - Tempo até casar deve ser menor que 1h (atual: {userStatus["timeUntilMarry"]})')
    
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
            print(f'Mensagem inválida detectada (erro {errorCount}/{maxErrors}), verificando status...')
            
            if errorCount >= maxErrors:
                print('Limite de erros atingido.')
                break
            
            userStatus = checkUserStatus()
            if userStatus['rollsRemaining'] == 0:
                print('Nenhum roll disponível após verificação.')
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
            print(f'\nAplicando marryLastRoll: {highestPowerCard["name"]} (Power: {highestPowerCard["power"]})')
            claimSuccess = claimCard(highestPowerCard['name'], highestPowerCard['idMessage'])
            
            if claimSuccess and Vars.divorceLastRoll:
                print(f'Divorciando {highestPowerCard["name"]}...')
                time.sleep(2)
                requests.post(url=url, headers=auth, data={'content': f'$divorce {highestPowerCard["name"]}'}) 
                time.sleep(2)
                requests.post(url=url, headers=auth, data={'content': 'y'})
                print('Divorce completo.')
    
    print('Rolling ended')

    if Vars.pokeRoll:
        print('\nTrying to roll Pokeslot')
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
