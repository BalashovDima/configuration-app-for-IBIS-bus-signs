from .romanize_ukrainian import romanize_ukrainian

def generate_zM_LCD_text_code(texts=[{'sign':'string','lcd':'string'}], indent=0):
    '''
    Generates code that displays text (text,that will be sent to IBIS using zM command) on LCD
    
    Returns a list of lines of the generated code

    Arguments:
    texts -- array of dictionaries with texts, text for lcd accessed by "lcd" key.
    indent -- number of spaces for the least indented part of the code
    '''
    code_lines = []
    indentation = indent * ' '

    for i, text in enumerate(texts):
        lcd_text = text['lcd']

        if(i == 0):
            code_lines.extend([
                f'{indentation}if(currect_InteriorSign_text_index == 0) {{\n',
                f'{indentation}    // length: {len(lcd_text)}\n'
                f'{indentation}    // {lcd_text}\n'
                f'{indentation}    lcd.print(F("{romanize_ukrainian(lcd_text)}"));\n',
                f'{indentation}}}\n'
            ])
        else:
            code_lines.pop()
            code_lines.extend([
                f'{indentation}}} else if(currect_InteriorSign_text_index == {i}) {{\n',
                f'{indentation}    // length: {len(lcd_text)}\n'
                f'{indentation}    // {lcd_text}\n'
                f'{indentation}    lcd.print(F("{romanize_ukrainian(lcd_text)}"));\n',
                f'{indentation}}}\n'
            ])

    return code_lines