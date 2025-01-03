import re
import sys

sys.path.append('src/modules/jpaw')
from pasteFormat import *

estructura = {
    "linkVipNormal": "https://vips.japan-vip.xyz/0:/",
    "linkVipEmision": "https://vips.japan-vip.xyz/1:/",
    "linkNormal": "https://anime.j-paw.xyz/0:down/",
    "linkEmision": "https://emision.j-paw.xyz/0:down/",
    "linkPubli1": "https://rinku.me/st?api=64f5521f1753a9373bd75e83158f2a6c5baaf44d&url=ouo.io/qs/1f3tWCLF?s=",
}
    

async def createPaste(status, routes):
    """
    Asynchronously creates a paste with VIP and normal links based on the given status and routes.
    Args:
        status (str): The status of the anime, either 'finalizado' or 'emision'.
        routes (list): A list of routes to be processed.
    Returns:
        tuple: A tuple containing:
            - The first route's second element (str).
            - The third element of the first route with the second element replaced by an empty string (str).
            - The generated paste (str).
    Raises:
        ValueError: If the status is not 'finalizado' or 'emision'.
    """
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
    
async def createNormalRoute(status, routes):
    """
    Asynchronously creates a list of URLs based on the given status and routes.
    Args:
        status (str): The status of the anime, either 'finalizado' or 'emision'.
        routes (list of list of str): A list of routes, where each route is a list of strings.
    Returns:
        list of str: A list of generated URLs if the status is valid.
        str: An error message if the status is invalid.
    Raises:
        None
    Notes:
        - The function uses the `estructura` dictionary to build the base URL.
        - The `normalizeText` function is used to normalize each item in the routes.
        - The `validUrl` function is used to validate the first URL in the response.
    """
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

async def newemisionCap(number, route):
    """
    Generates a formatted URL for a new chapter emission.

    Args:
        number (int): The chapter number.
        route (str): The route to be processed and appended to the base link.

    Returns:
        str: A formatted string containing the URL for the new chapter emission.

    """
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
    """
    Asynchronously processes a string of routes, splitting it into chapters and further sub-dividing each chapter.

    Args:
        routes (str): A string containing route information, with chapters separated by 'Drive'.

    Returns:
        list: A list of lists, where each inner list contains the segments of a chapter after splitting by '/'.
    """
    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[2:] for chapter in chapters]

async def clearRoutes(routes):
    """
    Asynchronously processes and clears routes from a given string.

    This function splits the input string by the keyword 'Drive', removes the first element,
    and then further splits each remaining element by '/'.

    Args:
        routes (str): A string containing the routes to be processed.

    Returns:
        list: A list of lists, where each inner list contains the segments of a route.
    """
    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[1:] for chapter in chapters]

async def normalizeText(routes):
    """
    Asynchronously normalizes a given text by replacing specific characters with their URL-encoded equivalents.

    Args:
        routes (str): The text to be normalized.

    Returns:
        str: The normalized text with specific characters replaced by their URL-encoded equivalents.
    """
    tratado2 = re.sub(r'\s', '%20', routes)
    tratado3 = re.sub(r'\[', '%5B', tratado2)
    tratado4 = re.sub(r'\]', '%5D', tratado3)
    tratado5 = re.sub(r',', '%2C', tratado4)
    tratado6 = re.sub(r'~', '%7E', tratado5)
    tratado7 = re.sub(r'[꞉]', '%ea%9e%89', tratado6)
    return re.sub(r'\?', '%3F', tratado7)

async def validUrl(url):
    """
    Checks if the given URL is valid by removing trailing '%20' and '/' characters.

    Args:
        url (str): The URL to be validated.

    Returns:
        str: The cleaned URL.
    """
    return url.rstrip('%20').rstrip('/')