from .transform_to_send_zM import transform_to_send_zM

def generate_zM_sending_code(texts, indent=0):
    '''
    Generates code that sends zM command
    
    Returns a list of lines of the generated code

    Arguments:
    texts -- array of dictionaries with texts to send to the sign accessed by "sign" key
    indent -- number of spaces for the least indented part of the code
    '''
    code_lines = []
    indentation = indent * ' '

    for i, text in enumerate(texts):
        sign_text = text["sign"]

        if(i == 0):
            code_lines.extend([
                f'{indentation}if(currect_InteriorSign_text_index == 0) {{\n',
                f'{indentation}    // length: {len(sign_text)}\n',
                f'{indentation}    // {sign_text}\n',
                f'{indentation}    IBIS_zM(F("{transform_to_send_zM(sign_text)}"));\n',
                f'{indentation}}}\n'
            ])
        else:
            code_lines.pop()
            code_lines.extend([
                f'{indentation}}} else if(currect_InteriorSign_text_index == {i}) {{\n',
                f'{indentation}    // length: {len(sign_text)}\n',
                f'{indentation}    // {sign_text}\n',
                f'{indentation}    IBIS_zM(F("{transform_to_send_zM(sign_text)}"));\n',
                f'{indentation}}}\n'
            ])

    return code_lines