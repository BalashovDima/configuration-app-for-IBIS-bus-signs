def transform_to_send_zM(text):
    '''Transforms Ukrainian text to text that can be send to the sign

    Replaces characters that cannot be send directy to the sign to the appropriate characters that are programmed in the sign to corespand get the wanted result   
    '''
    correspondence_info = {
        'А': 'A',
        'Б': 'B',
        'В': 'V',
        'Г': 'G',
        'Д': 'D',
        'Е': 'E',
        'Є': '>',
        'Ж': 'H',
        'З': 'Z',
        'И': 'I',
        'І': '@',
        'Ї': 'W',
        'Й': 'J',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'Ф': 'F',
        'Х': 'X',
        'Ц': 'C',
        'Ч': '^',
        'Ш': '<',
        'Щ': 'Q',
        'Ы': 'Y',
        'Ь': '*',
        'Ю': '$',
        'Я': '`',
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'є': '~',
        'ж': 'h',
        'з': 'z',
        'и': 'i',
        'і': '{',
        'ї': 'w',
        'й': 'j',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'x',
        'ц': 'c',
        'ч': '}',
        'ш': '\\\\',
        'щ': 'h',
        'ы': 'y',
        'ь': '?',
        'ю': '#',
        'я': '%'
    }

    transformed_text = ''

    for character in text:
        if(character in correspondence_info):
            transformed_text += correspondence_info[character]
        else:
            transformed_text += character

    return transformed_text