import os, sys, time, re
from pathlib import Path

sys.path.append('src/modules/jpaw')
from pasteFormat import *
from jpawPaste import estructura

def update_paste(path):
    """Continuously monitors a folder for changes and reports them.

    This function takes a folder path, creates an initial snapshot of its contents, and then periodically checks for changes, reporting any additions or removals.

    Args:
        path (str): The path to the folder to monitor.

    Returns:
        None
    """

    def initial_data(folder_path):
        """Creates a snapshot of the current contents of a folder.

        This function takes a folder path and returns a set containing the names of all files and subdirectories within that folder.

        Args:
            folder_path (str): The path to the folder.

        Returns:
            set: A set containing the names of all files and subdirectories in the specified folder.
        """

        return set(os.listdir(folder_path))
    
    data = initial_data(path)
    while True:
        check_folder_changes(path, data)
        data = initial_data(path)
        time.sleep(60)

def check_folder_changes(folder_path, initial_data):
    """Monitors a folder for changes by comparing its current contents to an initial snapshot.

    This function takes the path to a folder and a set representing its initial contents, then compares it to the current contents and reports any additions or removals.

    Args:
        folder_path (str): The path to the folder to monitor.
        initial_data (set): A set containing the initial file names in the folder.

    Returns:
        None
    """

    final_contents = set(os.listdir(folder_path))
    if changes := initial_data ^ final_contents:
        
        print(f"Changes detected in the folder: {changes}")
        
        for change in changes:
            if change in initial_data:
                print(f"File {change} was removed.")
            else:
                print(f"File {change} was added.")

                
    else:
        print("No changes detected in the folder.")
        
def updatePaste(status, routes):
    """Generates a formatted string containing links based on the status and routes provided.

    This function takes a status string and a routes string, processes them based on the status, and generates a formatted string containing VIP and normal links.

    Args:
        status (str): The status of the content (e.g., "finalizado", "emision").
        routes (str): The routes string containing file paths.

    Returns:
        tuple: A tuple containing the first route element, a modified route string, and the generated formatted string with links.  Returns 'Error en el estado del anime' if the status is not recognized.

    """

    if status.lower() == 'finalizado':
        routes = clearRoutesFin(routes)
        print(routes[0][0], routes[0][1])
        vipLink = f'\n{linkvipP1}{estructura["linkVipNormal"]}{normalizeText(routes[0][0])}/{normalizeText(routes[0][1])}/{linkvipP2}\n'
    elif status.lower() == 'emision':
        routes = clearRoutes(routes)
        vipLink = f'\n{linkvipP1}{estructura["linkVipEmision"]}{normalizeText(routes[0][0])}/{normalizeText(routes[0][1])}/{linkvipP2}\n'
    else: return 'Error en el estado del anime'
    paste = part1 + vipLink
    normalLinks = createNormalRoute(status, routes)
    chapters = 0
    for link in normalLinks:
        chapters += 1
        paste += f'[url={validUrl(link)}] Capitulo {chapters} [/url]\n'
    paste+='[/center]'
        
    return routes[0][1], f'{routes[0][2]}'.replace(routes[0][1], ''), paste

# Aux functions
def createNormalRoute(routes):
    for folder in os.listdir(routes):
        print(folder)
    
def clearRoutesFin(routes):
    """Processes a string containing file paths and extracts directory information.

    This function takes a string representing file paths, splits it based on the "Drive" keyword, and extracts the directory structure from each path segment, starting from the third element.

    Args:
        routes (str): The string containing file paths.

    Returns:
        list: A list of lists, where each inner list represents the directory structure of a path segment, excluding the first two elements.
    """

    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[2:] for chapter in chapters]

def clearRoutes(routes):
    """Processes a string containing file paths and extracts directory information.

    This function takes a string representing file paths, splits it based on the "Drive" keyword, and extracts the directory structure from each path segment.

    Args:
        routes (str): The string containing file paths.

    Returns:
        list: A list of lists, where each inner list represents the directory structure of a path segment.

    """

    chapters = routes.split('Drive')
    chapters = chapters[1:]
    return [chapter.split('/')[1:] for chapter in chapters]

def normalizeText(routes):
    """
    Normalizes text by replacing special characters with URL-encoded equivalents.

    This function takes a string and replaces certain characters with their corresponding URL-encoded values to ensure compatibility in various contexts.

    Args:
        routes (str): The text string to normalize.

    Returns:
        str: The normalized text string with URL-encoded characters.

    Examples:
        >>> normalizeText("hello world")
        'hello%20world'
        >>> normalizeText("example[1,2]?")
        'example%5B1%2C2%5D%3F'
    """

    tratado2 = re.sub(r'\s', '%20', routes)
    tratado3 = re.sub(r'\[', '%5B', tratado2)
    tratado4 = re.sub(r'\]', '%5D', tratado3)
    tratado5 = re.sub(r',', '%2C', tratado4)
    tratado6 = re.sub(r'~', '%7E', tratado5)
    tratado7 = re.sub(r'[꞉]', '%ea%9e%89', tratado6)
    return re.sub(r'\?', '%3F', tratado7)

def validUrl(url):
    """Cleans a URL by removing trailing spaces and slashes.

    This function takes a URL string and removes any trailing spaces (encoded as '%20') and forward slashes.

    Args:
        url (str): The URL string to clean.

    Returns:
        str: The cleaned URL string.

    Examples:
        >>> validUrl("https://example.com/%20/")
        'https://example.com'
        >>> validUrl("https://example.com/test%20")
        'https://example.com/test'
    """

    return url.rstrip('%20').rstrip('/')

if __name__ == '__main__':
    path = Path('C:/Users/Hime/Desktop/anime')
    createNormalRoute(path)