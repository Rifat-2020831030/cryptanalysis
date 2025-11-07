import string
from collections import Counter
import re

# English letter frequency distribution
english_freq = {
    'e': 12.22, 't': 9.67, 'a': 8.05, 'o': 7.63, 'i': 6.28, 'n': 6.95,
    's': 6.02, 'h': 6.62, 'r': 5.29, 'd': 5.10, 'l': 4.08, 'c': 2.23,
    'u': 2.92, 'm': 2.33, 'w': 2.60, 'f': 2.14, 'g': 2.30, 'y': 2.04,
    'p': 1.66, 'b': 1.67, 'v': 0.82, 'k': 0.95, 'j': 0.19, 'x': 0.11,
    'q': 0.06, 'z': 0.06
}

cipher1 = """af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao--wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc--pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi mddg oafg cepc tdvng qdfcafvi cei kiripkqe"""

cipher2 = """aceah toz puvg vcdl omj puvg yudqecov, omj loj auum klu thmjuv hs klu zlcvu shv zcbkg guovz, upuv zcmdu lcz vuwovroaeu jczoyyuovomdu omj qmubyudkuj vukqvm. klu vcdluz lu loj avhqnlk aodr svhw lcz kvopuez loj mht audhwu o ehdoe eunumj, omj ck toz yhyqeoveg auecupuj, tlokupuv klu hej sher wcnlk zog, klok klu lcee ok aon umj toz sqee hs kqmmuez zkqssuj tckl kvuozqvu. omj cs klok toz mhk umhqnl shv sowu, kluvu toz oezh lcz yvhehmnuj pcnhqv kh wovpue ok. kcwu thvu hm, aqk ck zuuwuj kh lopu eckkeu ussudk hm wv. aonncmz. ok mcmukg lu toz wqdl klu zowu oz ok scskg. ok mcmukg-mcmu klug aunom kh doee lcw tuee-yvuzuvpuj; aqk qmdlomnuj thqej lopu auum muovuv klu wovr. kluvu tuvu zhwu klok zlhhr klucv luojz omj klhqnlk klcz toz khh wqdl hs o nhhj klcmn; ck zuuwuj qmsocv klok omghmu zlhqej yhzzuzz (oyyovumkeg) yuvyukqoe ghqkl oz tuee oz (vuyqkujeg) cmubloqzkcaeu tuoekl. ck tcee lopu kh au yocj shv, klug zocj. ck czm'k mokqvoe, omj kvhqaeu tcee dhwu hs ck! aqk zh sov kvhqaeu loj mhk dhwu; omj oz wv. aonncmz toz numuvhqz tckl lcz whmug, whzk yuhyeu tuvu tceecmn kh shvncpu lcw lcz hjjckcuz omj lcz nhhj shvkqmu. lu vuwocmuj hm pczckcmn kuvwz tckl lcz vueokcpuz (ubduyk, hs dhqvzu, klu zodrpceeu-aonncmzuz), omj lu loj womg juphkuj ojwcvuvz owhmn klu lhaackz hs yhhv omj qmcwyhvkomk sowcecuz. aqk lu loj mh dehzu svcumjz, qmkce zhwu hs lcz ghqmnuv dhqzcmz aunom kh nvht qy. klu uejuzk hs kluzu, omj aceah'z sophqvcku, toz ghqmn svhjh aonncmz. tlum aceah toz mcmukg-mcmu lu ojhykuj svhjh oz lcz lucv, omj avhqnlk lcw kh ecpu ok aon umj; omj klu lhyuz hs klu zodrpceeu-aonncmzuz tuvu scmoeeg jozluj. aceah omj svhjh loyyumuj kh lopu klu zowu acvkljog, zuykuwauv 22mj. ghq loj aukkuv dhwu omj ecpu luvu, svhjh wg eoj, zocj aceah hmu jog; omj klum tu dom dueuavoku hqv acvkljog-yovkcuz dhwshvkoaeg khnukluv. ok klok kcwu svhjh toz zkcee cm lcz ktuumz, oz klu lhaackz doeeuj klu cvvuzyhmzcaeu ktumkcuz auktuum dlcejlhhj omj dhwcmn hs onu ok klcvkg-klvuu"""

def get_frequency(text):
    """Calculate frequency of each letter in the text"""
    letters = [c.lower() for c in text if c.isalpha()]
    total = len(letters)
    
    if total == 0:
        return {}
    
    # Count occurrences
    counts = Counter(letters)
    
    # Convert to percentages
    freq = {letter: (count / total) * 100 for letter, count in counts.items()}
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

def create_mapping_by_frequency(cipher_text):
    """Create initial mapping based on frequency analysis"""
    cipher_freq = get_frequency(cipher_text)
    
    # Sort English letters by frequency
    english_sorted = sorted(english_freq.keys(), key=lambda x: english_freq[x], reverse=True)
    cipher_sorted = list(cipher_freq.keys())
    
    mapping = {}
    for i, cipher_char in enumerate(cipher_sorted):
        if i < len(english_sorted):
            mapping[cipher_char] = english_sorted[i]
    
    return mapping

def apply_mapping(text, mapping):
    """Apply the substitution mapping to the text"""
    result = []
    for char in text:
        if char.lower() in mapping:
            mapped_char = mapping[char.lower()]
            result.append(mapped_char.upper() if char.isupper() else mapped_char)
        else:
            result.append(char)
    return ''.join(result)

def refine_mapping_interactive(cipher_text, mapping):
    """Refine mapping based on common patterns"""
    # Common English patterns 
    common_words = ['the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but']
    
    # Manual refinements based on analysis
    return mapping

def break_cipher(cipher_text, cipher_name):
    
    # Get frequency distribution
    cipher_freq = get_frequency(cipher_text)
    
    
    # Create initial mapping
    mapping = create_mapping_by_frequency(cipher_text)
    
    # Apply mapping
    decrypted = apply_mapping(cipher_text, mapping)
    
    print("\nInitial decryption attempt:")
    print(decrypted[:200] + "...")
    
    return decrypted, cipher_freq, mapping


decrypted1, freq1, map1 = break_cipher(cipher1, "CIPHER-1")

print("\n\n")

# Break Cipher 2
decrypted2, freq2, map2 = break_cipher(cipher2, "CIPHER-2")


# Cipher 1 refinement
# After analysis, we can see patterns suggesting specific mappings
refined_map1 = {
    'a': 'i', 'f': 'n', 'p': 'a', 'x': 'p', 'k': 'r', 'c': 't', 'q': 'c',
    'v': 'u', 'n': 'l', 'g': 'd', 'i': 'e', 'u': 'f', 'd': 'o', 'w': 'y',
    'e': 'h', 'o': 'm', 'h': 'b', 'j': 'q', 'r': 's', 't': 'w', 'l': 'k',
    'y': 'x', 'm': 'g', 's': 'z', 'b': 'v'
}

refined_dec1 = apply_mapping(cipher1, refined_map1)
print("\nCIPHER-1 Decrypted:")
print(refined_dec1)


# Cipher 2 refinement
refined_map2 = {
    'a': 'b', 'c': 'i', 'e': 'l', 'h': 'o', 't': 'w', 'o': 'a', 'z': 's',
    'p': 'v', 'u': 'e', 'v': 'r', 'd': 'c', 'l': 'h', 'm': 'a', 'j': 'd',
    'y': 'p', 'q': 'u', 'n': 'g', 's': 'f', 'r': 's', 'k': 't', 'g': 'y',
    'w': 'm', 'b': 'k', 'i': 'n', 'x': 'x', 's': 'f', 'q': 'u'
}

refined_dec2 = apply_mapping(cipher2, refined_map2)
print("\nCIPHER-2 Decrypted:")
print(refined_dec2)
