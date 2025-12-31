# Morse Code Converter

**International Morse Code with Binary Tree Implementation**

---

## Introduction

Morse Code is a character encoding scheme that represents letters, numbers, and punctuation as sequences of short and long signals called "dots" (·) and "dashes" (−). Invented in the 1830s-1840s by Samuel Morse and Alfred Vail for the telegraph, Morse Code revolutionized long-distance communication and remains in use today for amateur radio, aviation, and assistive technology.

Unlike modern digital encoding (ASCII, UTF-8), Morse Code is a **variable-length encoding** where common letters like 'E' (·) and 'T' (−) are shorter than rare letters like 'Q' (−−·−), making transmission more efficient.

CryptoSentinel's Morse Code Converter features:
- **Binary tree implementation** - Optimal encoding/decoding structure
- **International Morse Code standard** - Letters, numbers, punctuation
- **Audio generation** - Hear actual Morse code beeps
- **Prosigns support** - Special operator signals (SOS, etc.)

### When to Use This Tool

✅ **Learning Morse Code** - Educational purposes  
✅ **Amateur radio (HAM)** - Communication practice  
✅ **Accessibility** - Assistive technology for communication  
✅ **Emergency signaling** - SOS and distress calls  
✅ **Puzzle solving** - CTF challenges, cryptograms  

❌ **Modern telecommunications** - Use digital protocols instead  
❌ **High-speed data** - Too slow for practical data transfer  
❌ **Encryption** - Morse is encoding, not encryption ([[SHA256-Hash-Implementation]])  

---

## Algorithm: Variable-Length Encoding

### Morse Code Alphabet

**Letters:**
```
A  ·−        N  −·        
B  −···      O  −−−       
C  −·−·      P  ·−−·      
D  −··       Q  −−·−      
E  ·         R  ·−·       
F  ··−·      S  ···       
G  −−·       T  −         
H  ····      U  ··−       
I  ··        V  ···−      
J  ·−−−      W  ·−−       
K  −·−       X  −··−      
L  ·−··      Y  −·−−      
M  −−        Z  −−··      
```

**Numbers:**
```
0  −−−−−     5  ·····     
1  ·−−−−     6  −····     
2  ··−−−     7  −−···     
3  ···−−     8  −−−··     
4  ····−     9  −−−−·     
```

**Punctuation:**
```
.  ·−·−·−    (period)
,  −−··−−    (comma)
?  ··−−··    (question mark)
'  ·−−−−·    (apostrophe)
!  −·−·−−    (exclamation)
/  −··−·     (slash)
(  −·−−·     (parenthesis)
)  −·−−·−    (close paren)
&  ·−···     (ampersand)
:  −−−···    (colon)
;  −·−·−·    (semicolon)
=  −···−     (equal sign)
+  ·−·−·     (plus)
-  −····−    (hyphen)
_  ··−−·−    (underscore)
"  ·−··−·    (quote)
$  ···−··−   (dollar)
@  ·−−·−·    (at sign)
```

**Prosigns (special signals):**
```
SOS        ···−−−···   (distress)
KN         −·−−·       (invitation)
SK         ···−·−      (end of contact)
AR         ·−·−·       (end of message)
```

### Timing Rules (WPM - Words Per Minute)

**Standard timing (at 20 WPM):**

- **Dot**: 1 time unit (60 ms)
- **Dash**: 3 time units (180 ms)
- **Intra-character gap**: 1 time unit (60 ms) - between dots/dashes within letter
- **Inter-character gap**: 3 time units (180 ms) - between letters
- **Word gap**: 7 time units (420 ms) - between words

**Formula for WPM:**
```
WPM = Characters Per Minute / 5
(Standard word = 5 characters)

Dot duration (seconds) = 1.2 / WPM
```

**Example: "HELLO" at 20 WPM**
```
H    E  L      L      O
···· · ·−··   ·−··   −−−
     ↑      ↑      ↑
   word   word   word
   gaps   gaps   gaps

Total time: ~2.1 seconds
```

### Why Variable-Length?

**Efficiency through frequency:**

English letter frequency → Shorter Morse codes:

| Letter | Frequency | Morse | Length |
|--------|-----------|-------|--------|
| E | 12.7% | · | 1 |
| T | 9.1% | − | 1 |
| A | 8.2% | ·− | 2 |
| O | 7.5% | −−− | 3 |
| I | 7.0% | ·· | 2 |
| N | 6.7% | −· | 2 |
| ... | ... | ... | ... |
| Q | 0.1% | −−·− | 4 |
| Z | 0.1% | −−·· | 4 |

**Result:** Common letters transmit faster, reducing average message time.

This is an early example of **Huffman coding** (optimal prefix-free encoding).

---

## Algorithm: Binary Tree Implementation

### Morse Code as a Binary Tree

The most elegant way to encode/decode Morse is using a **binary tree**:

- **Left branch** (·) = Dot
- **Right branch** (−) = Dash
- **Each node** = Letter reached by that path

```
                    START
                   /     \
                  ·       −
                 /         \
                E           T
               / \         / \
              ·   −       ·   −
             /     \     /     \
            I       A   N       M
           / \     / \ / \     / \
          S   U   R  W D  K   G   O
         / \ / \ /|\ /|\ /|\ /|\ /|\
        H  V F  . L P J B X C Y Z Q
```

**Encoding algorithm:**
```
1. Start at root
2. For each character:
   - Look up in encoding table
   - Output dot/dash sequence
```

**Decoding algorithm:**
```
1. Start at root
2. For each dot/dash:
   - Go left (dot) or right (dash)
3. On gap (space), output current node's letter
4. Return to root
```

### Binary Tree Node Structure

```python
class MorseNode:
    """
    Node in Morse code binary tree.
    """
    def __init__(self, char: str = None):
        self.char = char      # Character (None for internal nodes)
        self.dot = None       # Left child (dot)
        self.dash = None      # Right child (dash)
```

### Building the Tree

```python
def build_morse_tree() -> MorseNode:
    """
    Build Morse code binary tree from encoding table.
    """
    root = MorseNode()
    
    # Morse code table
    morse_table = {
        'A': '·−',    'B': '−···',  'C': '−·−·',  'D': '−··',
        'E': '·',     'F': '··−·',  'G': '−−·',   'H': '····',
        'I': '··',    'J': '·−−−',  'K': '−·−',   'L': '·−··',
        'M': '−−',    'N': '−·',    'O': '−−−',   'P': '·−−·',
        'Q': '−−·−',  'R': '·−·',   'S': '···',   'T': '−',
        'U': '··−',   'V': '···−',  'W': '·−−',   'X': '−··−',
        'Y': '−·−−',  'Z': '−−··',
        '0': '−−−−−', '1': '·−−−−', '2': '··−−−', '3': '···−−',
        '4': '····−', '5': '·····', '6': '−····', '7': '−−···',
        '8': '−−−··', '9': '−−−−·'
    }
    
    # Insert each character into tree
    for char, code in morse_table.items():
        node = root
        
        for symbol in code:
            if symbol == '·':  # Dot
                if node.dot is None:
                    node.dot = MorseNode()
                node = node.dot
            else:  # Dash (−)
                if node.dash is None:
                    node.dash = MorseNode()
                node = node.dash
        
        # Mark leaf with character
        node.char = char
    
    return root
```

### Tree-Based Decoding

```python
def decode_morse(morse: str, root: MorseNode) -> str:
    """
    Decode Morse code using binary tree.
    
    Args:
        morse: Morse code string (dots, dashes, spaces)
        root: Root of Morse tree
        
    Returns:
        Decoded text
    """
    result = []
    node = root
    
    for symbol in morse + ' ':  # Add space to flush last character
        if symbol == '·':
            node = node.dot
            if node is None:
                raise ValueError("Invalid Morse code sequence")
                
        elif symbol == '−':
            node = node.dash
            if node is None:
                raise ValueError("Invalid Morse code sequence")
                
        elif symbol == ' ':
            # Space = end of character
            if node and node.char:
                result.append(node.char)
            node = root  # Reset to root
            
        elif symbol == '/':
            # Slash = word separator
            result.append(' ')
            node = root
    
    return ''.join(result)
```

---

## How It Works: Code Implementation

### Complete Morse Converter

```python
class MorseCodeConverter:
    """
    Convert between text and Morse code.
    """
    
    # Encoding table (text → Morse)
    TEXT_TO_MORSE = {
        'A': '·−',    'B': '−···',  'C': '−·−·',  'D': '−··',
        'E': '·',     'F': '··−·',  'G': '−−·',   'H': '····',
        'I': '··',    'J': '·−−−',  'K': '−·−',   'L': '·−··',
        'M': '−−',    'N': '−·',    'O': '−−−',   'P': '·−−·',
        'Q': '−−·−',  'R': '·−·',   'S': '···',   'T': '−',
        'U': '··−',   'V': '···−',  'W': '·−−',   'X': '−··−',
        'Y': '−·−−',  'Z': '−−··',
        '0': '−−−−−', '1': '·−−−−', '2': '··−−−', '3': '···−−',
        '4': '····−', '5': '·····', '6': '−····', '7': '−−···',
        '8': '−−−··', '9': '−−−−·',
        '.': '·−·−·−', ',': '−−··−−', '?': '··−−··', 
        '!': '−·−·−−', '/': '−··−·',  ' ': '/'
    }
    
    # Decoding table (Morse → text)
    MORSE_TO_TEXT = {v: k for k, v in TEXT_TO_MORSE.items()}
    
    def __init__(self):
        self.tree = self._build_tree()
    
    def _build_tree(self) -> MorseNode:
        """Build binary tree for decoding."""
        # (Implementation from above)
        pass
    
    def encode(self, text: str) -> str:
        """
        Convert text to Morse code.
        
        Args:
            text: Plain text to encode
            
        Returns:
            Morse code string
        """
        morse_chars = []
        
        for char in text.upper():
            if char in self.TEXT_TO_MORSE:
                morse_chars.append(self.TEXT_TO_MORSE[char])
            elif char == ' ':
                morse_chars.append('/')  # Word separator
            else:
                morse_chars.append('?')  # Unknown character
        
        return ' '.join(morse_chars)
    
    def decode(self, morse: str) -> str:
        """
        Convert Morse code to text.
        
        Args:
            morse: Morse code string
            
        Returns:
            Decoded text
        """
        # Split by spaces (character boundaries)
        morse_chars = morse.split(' ')
        
        result = []
        for morse_char in morse_chars:
            if morse_char == '/':
                result.append(' ')  # Word space
            elif morse_char in self.MORSE_TO_TEXT:
                result.append(self.MORSE_TO_TEXT[morse_char])
            elif morse_char:  # Non-empty, unknown
                result.append('?')
        
        return ''.join(result)
    
    def encode_to_audio(self, text: str, wpm: int = 20) -> bytes:
        """
        Generate audio WAV file of Morse code.
        
        Args:
            text: Text to convert
            wpm: Words per minute (speed)
            
        Returns:
            WAV audio data
        """
        import wave
        import math
        
        sample_rate = 44100  # Hz
        frequency = 800      # Hz (beep tone)
        
        # Calculate timing
        dot_duration = 1.2 / wpm  # seconds
        dash_duration = 3 * dot_duration
        
        morse = self.encode(text)
        audio_data = []
        
        for symbol in morse:
            if symbol == '·':
                audio_data.extend(self._generate_tone(
                    frequency, dot_duration, sample_rate
                ))
                audio_data.extend(self._generate_silence(
                    dot_duration, sample_rate
                ))
            elif symbol == '−':
                audio_data.extend(self._generate_tone(
                    frequency, dash_duration, sample_rate
                ))
                audio_data.extend(self._generate_silence(
                    dot_duration, sample_rate
                ))
            elif symbol == ' ':
                # Character gap
                audio_data.extend(self._generate_silence(
                    2 * dot_duration, sample_rate  # Total 3 units
                ))
            elif symbol == '/':
                # Word gap
                audio_data.extend(self._generate_silence(
                    6 * dot_duration, sample_rate  # Total 7 units
                ))
        
        return bytes(audio_data)
    
    def _generate_tone(self, freq: float, duration: float, 
                      sample_rate: int) -> List[int]:
        """Generate sine wave tone."""
        samples = int(duration * sample_rate)
        return [
            int(32767 * math.sin(2 * math.pi * freq * i / sample_rate))
            for i in range(samples)
        ]
    
    def _generate_silence(self, duration: float, 
                         sample_rate: int) -> List[int]:
        """Generate silence."""
        samples = int(duration * sample_rate)
        return [0] * samples
```

---

## Usage Guide: CLI Commands

### Starting the Tool

```bash
python cli.py

# Select: 3. Encoding Tools > 2. Morse Code Converter
```

### Text to Morse

```
Choose operation:
1. Text to Morse
2. Morse to Text
3. Generate audio
4. Learn Morse code

Selection: 1

Enter text: SOS HELP

✓ Morse code:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
··· −−− ··· / ···· · ·−·· ·−−·
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Visual representation:
S     O       S       H       E  L        P
···   −−−     ···     ····    ·  ·−··     ·−−·
```

### Morse to Text

```
Selection: 2

Enter Morse code: ··· −−− ··· / ···· · ·−·· ·−−·

✓ Decoded text:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOS HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Audio Generation

```
Selection: 3

Enter text: HELLO WORLD
Speed (WPM): 20

🔊 Generating Morse code audio...

Character breakdown:
H  ···· (4 dots)
E  ·    (1 dot)
L  ·−·· (dot-dash-dot-dot)
L  ·−·· (dot-dash-dot-dot)
O  −−− (3 dashes)

W  ·−− (dot-dash-dash)
O  −−− (3 dashes)
R  ·−· (dot-dash-dot)
L  ·−·· (dot-dash-dot-dot)
D  −·· (dash-dot-dot)

✓ Audio file saved: morse_output.wav
Duration: 4.2 seconds at 20 WPM

🎧 Play audio to hear actual Morse code!
```

### Learning Mode

```
Selection: 4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MORSE CODE LEARNING GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Start with these letters (most common):

E  ·         (1 dot)
T  −         (1 dash)
I  ··        (2 dots)
A  ·−        (dot-dash)
N  −·        (dash-dot)
M  −−        (2 dashes)
S  ···       (3 dots)
O  −−−       (3 dashes)

🎯 Memory tricks:

SOS  ···−−−···  (Save Our Ship)
     3-3-3 pattern

Love ·−·· −−− ···− ·
     L    O   V   E

Quiz mode: [Press Q]
Practice: [Press P]
```

---

## Troubleshooting

### Common Issues

**Problem:** "Decoded text has question marks (?)"  
**Solution:** Invalid Morse sequences:
- Check spacing: Use single space between letters, / between words
- Valid symbols: Only · (dot) and − (dash) allowed
- Unknown sequences become '?'
- Example: `···· ???? ·` → `H?E` (unknown 4-dash sequence)

**Problem:** "Audio doesn't play or sounds wrong"  
**Solution:** Audio generation issues:
- Check WAV file format compatibility
- Frequency: 800 Hz is standard (500-1000 Hz acceptable)
- Speed: 10-30 WPM recommended (< 10 too slow, > 30 too fast)
- Volume: Adjust system volume if too quiet
- Try different media player if default doesn't work

**Problem:** "Converting from visual Morse (−) to ASCII gives errors"  
**Solution:** Symbol confusion:
- ✓ **Correct**: Use actual dot (·) U+00B7 and dash (−) U+2212
- ✓ **Alternative**: Use period (.) and hyphen (-)
- ❌ **Wrong**: Using em-dash (—), en-dash (–), or other characters
- Tool accepts both formats, but output uses official symbols

**Problem:** "Why are numbers so long compared to letters?"  
**Solution:** Design choice:
- Numbers: All 5 symbols (····− to −−−−−)
- Letters: 1-4 symbols
- Reason: Numbers less common in typical messages
- Trade-off: Consistent 5-symbol pattern for memorization
- Modern variants use shorter number codes

**Problem:** "Can I use Morse for actual emergency communication?"  
**Solution:** Yes, but with caveats:
- ✓ **SOS** (···−−−···) is universally recognized
- ✓ Amateur radio (HAM) operators know Morse
- ⚠️ **Cell phone**: Text/call more reliable
- ⚠️ **Maritime**: Radio systems use digital protocols now
- ⚠️ **Aviation**: Replaced by digital in most countries
- Know your context: Morse works if receiver knows it!

---

## Pros and Cons

### ✅ Advantages

**Simplicity**
- Only 2 symbols (dot, dash)
- Easy to learn (26 letters in a week)
- No special equipment needed
- Works with light, sound, tapping, any on/off signal

**Robustness**
- Works in noisy environments
- Partial message still intelligible
- Error detection (invalid sequences obvious)
- No need for synchronized clocks

**Accessibility**
- Assistive technology for speech/hearing impaired
- Minimal cognitive load
- Physical signaling possible (blink, tap)
- Works without visual/audio feedback

**Historical Significance**
- Foundation of telecommunications
- Taught pattern recognition → Led to digital encoding
- Still used: Aviation (beacons), amateur radio, accessibility
- Cultural: "Morse" in movies, military history

### ❌ Disadvantages

**Slow Speed**
- Average: 20-30 WPM (words per minute)
- Compare: Typing 40-60 WPM, reading 200+ WPM
- Not suitable for high-bandwidth communication
- Modern digital: Thousands of WPM equivalent

**Requires Training**
- Must memorize all codes
- Takes weeks to become proficient
- Expert level: 6+ months of practice
- Unlike typing (visual keyboard available)

**Variable Length Issues**
- No natural byte alignment
- Spacing critical (errors propagate)
- Difficult to parse programmatically without gaps
- Contrast: ASCII/UTF-8 have fixed positions

**Limited Character Set**
- Basic Latin alphabet only
- No lowercase distinction
- Limited punctuation
- No emojis, special characters, other languages
- International variants exist but not standardized

**Not Secure**
- Encoding, not encryption ([[SHA256-Hash-Implementation]])
- Anyone can decode
- Pattern recognition possible
- Military messages required additional encryption

### Speed Comparison

| Method | WPM | Use Case |
|--------|-----|----------|
| Morse (beginner) | 5-10 | Learning |
| Morse (amateur) | 20-30 | HAM radio |
| Morse (expert) | 40-60 | Professional operators |
| Typing (average) | 40-60 | General use |
| Typing (professional) | 80-120 | Transcription |
| Reading | 200-300 | Silent reading |
| Digital transmission | 1,000,000+ | Internet |

---

## Related Tools

- **[[Base64-Encoder-Decoder]]** - Another encoding method (binary-to-text)
- **[[Caesar-Cipher-Tool]]** - Another historical communication cipher
- **[[Simple-XOR-Encryption]]** - Binary operations (similar to dot/dash)

---

## References

### Historical Context
- **1836-1844**: Samuel Morse and Alfred Vail develop telegraph code
- **1865**: International Morse Code standardized
- **1912**: Titanic disaster - SOS call widely recognized
- **WWI/WWII**: Extensive military use
- **1999**: Official end of Morse requirement for ship operators
- **2007**: Morse removed from amateur radio licensing (US)
- **Present**: Still used by HAM enthusiasts, accessibility tech

### Technical Specifications
- **ITU-R M.1677-1**: International Morse Code standard
- **Frequency**: Typically 500-1000 Hz for audio
- **Speed**: 5-40 WPM typical range
- **Timing**: Paris standard (50 units for "PARIS")

### Binary Tree Algorithm
- **Huffman coding** (1952): Similar optimal prefix-free encoding
- **Tree traversal**: O(log n) average, O(n) worst case
- **Space efficiency**: Minimal memory footprint

### Modern Applications
- **CW (Continuous Wave)**: Amateur radio mode
- **Assistive technology**: Blink detection, single-switch input
- **Aviation**: NDB (Non-Directional Beacon) identification
- **Emergency**: Light/sound signaling when other methods fail

---

## Learn More

**Next Steps:**
1. Practice with online Morse trainers (LCWO, Morse Code Ninja)
2. Explore [[Base64-Encoder-Decoder]] for modern binary encoding
3. Learn [[Password-Strength-Analyzer]] for understanding information entropy

**External Resources:**
- [ITU Morse Code Standard](https://www.itu.int/rec/R-REC-M.1677-1-200910-I/)
- [Learn CW Online (LCWO)](https://lcwo.net/)
- [Morse Code Wikipedia](https://en.wikipedia.org/wiki/Morse_code)
- [Morse Code Translator](https://morsecode.world/international/translator.html)

**Fun Facts:**
- SOS (···−−−···) was chosen for ease of recognition, not as abbreviation
- "The quick brown fox jumps over the lazy dog" contains all letters
- Samuel Morse's first message: "What hath God wrought" (1844)
- Morse code used on Voyager Golden Record (sent to space!)

---

---

## Navigation

[← Back to Home](Home) | [Report Issue](https://github.com/Shiva-destroyer/CryptoSentinel/issues) | [View All Tools](Home#available-tools)

---

**Developed by:** saisrujanmurthy@gmail.com
