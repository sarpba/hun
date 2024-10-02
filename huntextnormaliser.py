import re
from datetime import datetime

class HungarianTextNormalizer:
    def __init__(self):
        # Szótárak és minták inicializálása
        self.months = {
            'jan': 'január',
            'feb': 'február',
            'márc': 'március',
            'ápr': 'április',
            'máj': 'május',
            'jún': 'június',
            'júl': 'július',
            'aug': 'augusztus',
            'szept': 'szeptember',
            'okt': 'október',
            'nov': 'november',
            'dec': 'december'
        }
        self.weekdays = {
            'h': 'hétfő',
            'k': 'kedd',
            'sze': 'szerda',
            'cs': 'csütörtök',
            'p': 'péntek',
            'szo': 'szombat',
            'v': 'vasárnap'
        }
        self.currency_symbols = {
            '$': 'dollár',
            '€': 'euró',
            '£': 'font',
            '¥': 'jen',
            '₽': 'rubel',
            'HUF': 'forint',
            'Ft': 'forint'
        }
        self.math_symbols = {
            '+': 'plusz',
            '-': 'mínusz',
            '*': 'szorozva',
            '/': 'osztva',
            '=': 'egyenlő',
            '%': 'százalék'
        }
        self.spoken_symbols = {
            '(': 'zárójel nyitva',
            ')': 'zárójel zárva',
            '"': 'idézőjel',
            "'": 'aposztróf'
        }
        self.units = {
            '°C': 'fok Celsius',
            '°F': 'fok Fahrenheit',
            'K': 'kelvin',
            't': 'tonna',
            'q': 'mázsa',
            'kg': 'kilogramm',
            'dkg': 'dekagramm',
            'g': 'gramm',
            'mg': 'milligramm',
            'μg': 'mikrogramm',
            'l': 'liter',
            'dl': 'deciliter',
            'cl': 'centiliter',
            'ml': 'milliliter',
            'km': 'kilométer',
            'm': 'méter',
            'dm': 'deciméter',
            'cm': 'centiméter',
            'mm': 'milliméter',
            'μm': 'mikrométer',
            'nm': 'nanométer',
            'ha': 'hektár',
            'a': 'ár',
            'bar': 'bar',
            'Pa': 'pascal',
            'hPa': 'hektopascal',
            'kPa': 'kilopascal',
            'MPa': 'megapascal',
            's': 'másodperc',
            'min': 'perc',
            'h': 'óra',
            'Hz': 'hertz',
            'kHz': 'kilohertz',
            'MHz': 'megahertz',
            'GHz': 'gigahertz',
            'A': 'amper',
            'V': 'volt',
            'W': 'watt',
            'kW': 'kilowatt',
            'kWh': 'kilowattóra',
            'm²': 'négyzetméter',
            'm³': 'köbméter',
            'Mbps': 'megabit per szekundum',
            'Gbps': 'gigabit per szekundum',
            'B': 'byte',
            'KB': 'kilobyte',
            'MB': 'megabyte',
            'GB': 'gigabyte',
            'TB': 'terabyte',
            # További mértékegységek szükség szerint
        }

    def accent_peculiarity(self, text):
        # Unicode furcsaságok eltávolítása
        replacements = {
            'ﬁ': 'fi',
            'ﬂ': 'fl',
            '’': "'",
            '“': '"',
            '”': '"',
            '–': '-',
            '—': '-',
            '˚': '°'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def acronym_phoneme(self, text):
        # Betűszavak fonémikus átírása
        def replace_acronyms(match):
            acronym = match.group(0)
            letters = ' '.join([self.letter_to_phoneme(c) for c in acronym])
            return letters

        return re.sub(r'\b[A-ZÁÉÍÓÖŐÚÜŰ]{2,}\b', replace_acronyms, text)

    def letter_to_phoneme(self, letter):
        # Betűk átírása fonémára
        phonemes = {
            'A': 'á', 'B': 'bé', 'C': 'cé', 'D': 'dé', 'E': 'é',
            'F': 'ef', 'G': 'gé', 'H': 'há', 'I': 'í', 'J': 'jé',
            'K': 'ká', 'L': 'el', 'M': 'em', 'N': 'en', 'O': 'ó',
            'P': 'pé', 'Q': 'kú', 'R': 'er', 'S': 'es', 'T': 'té',
            'U': 'ú', 'V': 'vé', 'W': 'dupla vé', 'X': 'iksz', 'Y': 'ipszilon', 'Z': 'zé',
            'Á': 'á', 'É': 'é', 'Í': 'í', 'Ó': 'ó', 'Ö': 'ő',
            'Ő': 'ő', 'Ú': 'ú', 'Ü': 'ű', 'Ű': 'ű'
        }
        return phonemes.get(letter.upper(), letter)

    def amount_money(self, text):
        # Pénznemek átírása
        pattern = re.compile(r'(\d+[\d\s,.]*)\s*([€$£¥₽]|HUF|Ft)')
        def replace_currency(match):
            amount = match.group(1)
            currency = self.currency_symbols.get(match.group(2), match.group(2))
            return f"{amount} {currency}"
        return pattern.sub(replace_currency, text)

    def date(self, text):
        # Dátumok átírása
        pattern = re.compile(r'(\d{1,2})\.(\d{1,2})\.(\d{4})')
        def replace_date(match):
            day, month, year = match.groups()
            month_name = self.months.get(month.lstrip('0'), f"{month}. hónap")
            return f"{year}. {month_name} {int(day)}."
        return pattern.sub(replace_date, text)

    def timestamp(self, text):
        # Időbélyegek átírása
        pattern = re.compile(r'(\d{1,2})h:(\d{1,2})m:(\d{1,2})s')
        def replace_timestamp(match):
            hours, minutes, seconds = match.groups()
            return f"{int(hours)} óra {int(minutes)} perc {int(seconds)} másodperc"
        return pattern.sub(replace_timestamp, text)

    def time_of_day(self, text):
        # Napi időpontok átírása
        pattern = re.compile(r'(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?h?')
        def replace_time(match):
            hours, minutes, seconds = match.groups()
            result = f"{int(hours)} óra {int(minutes)} perc"
            if seconds:
                result += f" {int(seconds)} másodperc"
            return result
        return pattern.sub(replace_time, text)

    def weekday(self, text):
        # Hét napjainak rövidítéseinek átírása
        for abbr, full in self.weekdays.items():
            text = re.sub(rf'\b{abbr}\b', full, text, flags=re.IGNORECASE)
        return text

    def month(self, text):
        # Hónapok rövidítéseinek átírása
        for abbr, full in self.months.items():
            text = re.sub(rf'\b{abbr}\b', full, text, flags=re.IGNORECASE)
        return text

    def ordinal(self, text):
        # Sorszámok átírása
        pattern = re.compile(r'\b(\d+)\.')
        def replace_ordinal(match):
            number = int(match.group(1))
            ordinal = self.number_to_ordinal(number)
            return ordinal
        return pattern.sub(replace_ordinal, text)

    def number_to_ordinal(self, number):
        # Sorszám számának átírása szöveggé
        ordinals = {
            1: 'első',
            2: 'második',
            3: 'harmadik',
            4: 'negyedik',
            5: 'ötödik',
            6: 'hatodik',
            7: 'hetedik',
            8: 'nyolcadik',
            9: 'kilencedik',
            10: 'tizedik',
            11: 'tizenegyedik',
            12: 'tizenkettedik',
            # Bővíthető tovább szükség szerint
        }
        return ordinals.get(number, f"{number}.")  # Ha nincs benne, visszaadja a számot ponttal

    def special(self, text):
        # Különleges esetek átírása
        pattern = re.compile(r'(\d+)/(\d+)')
        def replace_fraction(match):
            numerator, denominator = match.groups()
            return f"{numerator} a {denominator}-ből"
        return pattern.sub(replace_fraction, text)

    def math_symbol(self, text):
        # Matematikai szimbólumok átírása
        for symbol, word in self.math_symbols.items():
            # Biztosítjuk, hogy ne cserélje le a szimbólumokat szavakon belül
            text = re.sub(rf'(?<!\S){re.escape(symbol)}(?=\s|$)', f" {word} ", text)
        return text

    def spoken_symbol(self, text):
        # Beszélt szimbólumok átírása
        for symbol, word in self.spoken_symbols.items():
            text = text.replace(symbol, f" {word} ")
        return text

    def units_of_measurement(self, text):
        # Mértékegységek átírása
        pattern = re.compile(r'(\b\d+[\d\s,\.]*)\s*([°˚]?[A-Za-zμ²³]+)\b')
        def replace_units(match):
            amount = match.group(1)
            unit = match.group(2)
            unit_full = self.units.get(unit, unit)
            return f"{amount} {unit_full}"
        return pattern.sub(replace_units, text)

    def remove_extra_spaces(self, text):
        # Felesleges szóközök eltávolítása
        return re.sub(r'\s+', ' ', text).strip()

    def normalize(self, text):
        # Teljes szöveg normalizálása
        text = self.accent_peculiarity(text)
        text = self.acronym_phoneme(text)
        text = self.amount_money(text)
        text = self.date(text)
        text = self.timestamp(text)
        text = self.time_of_day(text)
        text = self.weekday(text)
        text = self.month(text)
        text = self.ordinal(text)
        text = self.special(text)
        text = self.math_symbol(text)
        text = self.spoken_symbol(text)
        text = self.units_of_measurement(text)
        text = self.remove_extra_spaces(text)
        # További normalizálási lépések szükség szerint
        return text

# Példa használatra
if __name__ == "__main__":
    normalizer = HungarianTextNormalizer()
    sample_text = """
    Az időpont 13h:15m:45s volt.

    A hőmérséklet ma +25°C lesz, holnap pedig -5°C.
    
    A tömeg 70kg, ami 0.07t-nak felel meg.
    A távolság 5km, amelyet 30min alatt tettünk meg.
    A terület 10ha, amely 100000m²-nek felel meg.
    A folyadék térfogata 2.5l, vagyis 2500ml.
    Az adatátvitel sebessége 100Mbps.
    A fájl mérete 2GB.
    A feszültség 230V, az áramerősség 10A.
    Az ABC rövidítés jelentése: American Broadcasting Company.
    """
    normalized_text = normalizer.normalize(sample_text)
    print(normalized_text)
