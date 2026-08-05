MORSE_CODE = {
    'A': '.-',  'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', 
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', 
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', 
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', 
    '$': '...-..-', '@': '.--.-.', 
    ' ': '/'

}

MORSE_JA = {
    # ア行
    'あ': '--.--', 'い': '.-', 'う': '..-', 'え': '-.---', 'お': '.-...',
    # カ行
    'か': '.-..', 'き': '-.-..', 'く': '...-', 'け': '-.--', 'こ': '----',
    # サ行
    'さ': '-.-.-', 'し': '--.-.', 'す': '---.-', 'せ': '.---.', 'そ': '---.',
    # タ行
    'た': '-.', 'ち': '..-.', 'つ': '.--.', 'て': '-.-.--', 'と': '..--.',
    # ナ行
    'な': '-.-', 'に': '-.-.', 'ぬ': '....', 'ね': '--.-', 'の': '..--',
    # ハ行
    'は': '-...', 'ひ': '--..-', 'ふ': '--..', 'へ': '.', 'ほ': '-..',
    # マ行
    'ま': '-..-', 'み': '..--.-', 'む': '-', 'め': '-...', 'ﾓ': '-..-.',  # 'も'
    # ヤ行
    'や': '.--', 'ゆ': '-..--', 'よ': '--',
    # ラ行
    'ら': '...', 'り': '--.', 'る': '-.--.', 'れ': '---', 'ろ': '.-.-',
    # ワ行
    'わ': '-.-', 'ゐ': '.-..-', 'ゑ': '.-..', 'を': '.---',
    # 拨音
    'ん': '.-.-.',
    # 符号及浊音标记
    '゛': '..',        # 浊点 (Dakuten)
    '゜': '--..-',     # 半浊点 (Handakuten)
    'ー': '.--.-'      # 长音符 (Chouonpu)
}

def encode_mixed(text):
    result = []
    for char in text:
        if char in MORSE_JA:
            result.append(MORSE_JA[char])
        elif char in MORSE_CODE:
            result.append(MORSE_CODE[char])
        else:
            result.append('?')
    return ' '.join(result)

def encode_unicode(text):
    result = []
    for char in text:
        code_point = str(ord(char))
        morse_num = ' '.join(MORSE_CODE.get(d, '') for d in code_point)
        result.append(morse_num)
    return ' / '.join(result)

def encode(text):
    text = text.upper()
    result = []
    for char in text:
        if char in MORSE_CODE:
            result.append(MORSE_CODE[char])
        else:
            result.append('?')
    return ' '.join(result)

def decode(morse):
    morse = morse.strip()
    reverse_dict = {v: k for k, v in MORSE_CODE.items()}
    words = morse.split(' / ')
    decode_words = []
    for word in words:
        letters = word.split(' ')
        decode_word = ''.join(reverse_dict.get(code, "?") for code in letters)
        decode_words.append(decode_word)
    return ' '.join(decode_words)

def auto_encode(text):
    has_japanese = any('\u3040' <= char <= '\u30FF' for char in text)
    if has_japanese:
        return encode_mixed(text)
    else:
        return encode(text)
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(encode(text))
    else:
        user_input = input("please add the text to convert: ")

        if user_input.strip() == "":
            text = "That kid's long gone and this old man's all that's left. I gotta live with that,"
            print(f" defualt content: \n{text}\n")
        else:
            test = user_input
            print(f"\n encoding: {text}\n")

        print(encode(text))
