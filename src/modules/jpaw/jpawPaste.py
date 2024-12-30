import re, os
from modules.jpaw.pasteFormat import *
import sys

sys.path.append('src/modules/jpaw')

estructura = {
    "linkVipNormal": "https://vips.japan-vip.xyz/0:/",
    "linkVipEmision": "https://vips.japan-vip.xyz/1:/",
    "linkNormal": "https://anime.j-paw.xyz/0:down/",
    "linkEmision": "https://emision.j-paw.xyz/0:down/",
    "linkPubli1": "https://rinku.me/st?api=64f5521f1753a9373bd75e83158f2a6c5baaf44d&url=ouo.io/qs/1f3tWCLF?s=",
}
    
async def createNormalRoute(status, routes):
    chapters = 0
    response = []
    
    if status.lower() == 'finalizado': 
        for items in routes:
            paste = f'{estructura["linkNormal"]}'
            chapters += 1
            for item in items:
                if item == items[-1]:
                    paste += f'{await normalizeText(item)}'
                else:
                    paste += f'{await normalizeText(item)}/'
            response.append(f'{estructura["linkPubli1"]}{await validUrl(paste)}' if chapters == 1 else paste)
        return response
    
    elif status.lower() == 'emision':
        for items in routes:
            paste = f'{estructura["linkEmision"]}'
            chapters += 1
            for item in items:
                if item == items[-1]:
                    paste += f'{await normalizeText(item)}'
                else:
                    paste += f'{await normalizeText(item)}/'
            response.append(f'{estructura["linkPubli1"]}{await validUrl(paste)}' if chapters == 1 else paste)
        return response
    else: return 'Error en el estado del anime'

async def createPaste(status, routes):
    if status.lower() == 'finalizado':
        routes = await clearRoutesFin(routes)
        print(routes[0][0], routes[0][1])
        vipLink = f'\n{linkvipP1}{estructura["linkVipNormal"]}{await normalizeText(routes[0][0])}/{await normalizeText(routes[0][1])}/{linkvipP2}\n'
    elif status.lower() == 'emision':
        routes = await clearRoutes(routes)
        vipLink = f'\n{linkvipP1}{estructura["linkVipEmision"]}{await normalizeText(routes[0][0])}/{await normalizeText(routes[0][1])}/{linkvipP2}\n'
    else: return 'Error en el estado del anime'
    paste = part1 + vipLink
    normalLinks = await createNormalRoute(status, routes)
    chapters = 0
    for link in normalLinks:
        chapters += 1
        paste += f'[url={await validUrl(link)}] Capitulo {chapters} [/url]\n'
    paste+='[/center]'
        
    return routes[0][1], f'{routes[0][2]}'.replace(routes[0][1], ''), paste

async def newemisionCap(number, route):
    routes = await clearRoutes(route)
    link = f'{estructura["linkEmision"]}'
    for items in routes:
        for item in items:
            if item == items[-1]:
                link += f'{await normalizeText(item)}'
            else:
                link += f'{await normalizeText(item)}/'
    return f'[url={await validUrl(link)}] Capitulo {number} [/url]\n'


# Aux functions
async def clearRoutesFin(routes):
    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[2:] for chapter in chapters]

async def clearRoutes(routes):
    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[1:] for chapter in chapters]

async def normalizeText(routes):
    tratado2 = re.sub(r'\s', '%20', routes)
    tratado3 = re.sub(r'\[', '%5B', tratado2)
    tratado4 = re.sub(r'\]', '%5D', tratado3)
    tratado5 = re.sub(r',', '%2C', tratado4)
    tratado6 = re.sub(r'~', '%7E', tratado5)
    tratado7 = re.sub(r'[꞉]', '%ea%9e%89', tratado6)
    return re.sub(r'\?', '%3F', tratado7)

async def validUrl(url):
    return url.rstrip('%20').rstrip('/')