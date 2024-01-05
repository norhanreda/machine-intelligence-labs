from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

# def caesar_dechiper(ciphered: str) -> DechiperResult:
def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:    
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # utils.NotImplemented()
   

    final_set = []
    asci_codes = [ord(char) for char in ciphered]
    dict_set = set(dictionary)

    for shift in range(1, 27):
        shifted_asci_codes = [(asci - 97 - shift) % 26 + 97 if asci != 32 else asci for asci in asci_codes]
        text = ''.join(chr(code) for code in shifted_asci_codes)
        values = text.split(" ")
        non_dictionary_words = sum(1 for word in values if word.lower() not in dict_set)
        final_set.append((text, shift, non_dictionary_words))

    res = min(final_set, key=lambda x: x[2])
    return res
 





