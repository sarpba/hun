# Magyar Szövegnormalizáló F5-TTS-hez

Ez a szkript, a `normaliser.py`, magyar szövegek előfeldolgozására szolgál, fonetikailag explicitebb alakra konvertálva azokat. Ez a normalizált szöveg különösen alkalmas Text-to-Speech (TTS) rendszerek, például az F5-TTS bemeneteként, a szintetizált beszéd minőségének és természetességének javítása érdekében.

A szkript számos szövegnormalizálási feladatot hajt végre, beleértve a számok, dátumok, mozaikszavak és egyéb gyakori szöveges konvenciók kezelését, átalakítva azokat egy olyan formátumba, amelyet egy TTS motor könnyebben tud helyesen kiejteni magyarul.

## Normalizálási Lépések

A `normaliser.py` szkript a következő átalakításokat hajtja végre sorrendben:

1.  **Római Számok Átalakítása (`replace_roman_numerals`):** Ponttal végződő római számokat (pl. "IV.") arab számokká alakít (pl. "4.").
2.  **Időformátumok Kezelése (`replace_times`):** Időpontokat (pl. "7:30-kor", "08:00", "22:15:30") beszélt magyar nyelvi alakra hoz. Véletlenszerűen választ az "óra perc perc" és "óra perc" formátumok között, ha nincs másodperc. Másodpercek esetén az "óra perc másodperc" formátumot használja. A "-kor" ragokat kezeli.
3.  **Kényszerített Cserék Alkalmazása (`apply_force_changes`):** Közvetlen rész-sztring cseréket hajt végre a `force_changes.csv` fájl alapján. Ez lehetővé teszi a sztring-átalakítások finomhangolását, beleértve a szóközök hozzáadását a kicserélt kifejezés előtt vagy után.
4.  **Általános Cserék Alkalmazása (`apply_changes`):** Teljes szavas, kis- és nagybetűket nem megkülönböztető cseréket hajt végre a `changes.csv` fájl alapján.
5.  **Mozaikszavak Kiejtése (`replace_acronyms`):** Betűnként ejti ki a mozaikszavakat (két vagy több nagybetűből álló szavak, pl. "NATO" -> "en á té ó"). A római számok kivételt képeznek ez alól.
6.  **Alfanumerikus Szavak Kezelése (`replace_alphanumeric`):** Betűket és számokat egyaránt tartalmazó szavakat (pl. "B2", "K-9") dolgoz fel. A betűket betűnként ejti, a számokat pedig szavakká alakítja (pl. "bé kettő", "ká kilenc").
7.  **Dátumformázás (`replace_dates`):** Különböző magyar dátumformátumokat (pl. "2025. június 1.", "2025. 06. 01.", "2025.VI.1.", "2021-05-20") egységes beszélt alakra hoz (pl. "kétezer-huszonöt június elseje"). Kezeli a teljes hónapneveket, rövidített hónapneveket, számos hónapokat és római számos hónapokat.
8.  **Sorszámnevek Átalakítása (`replace_ordinals`):** Ponttal végződő sorszámneveket (pl. "4.") magyar szavas alakra alakít (pl. "negyedik"). Ez a lépés kihagyja az évszámokat és a mondat végén, írásjel előtt álló számokat.
9.  **Tőszámnevek Átalakítása (`replace_numbers`):** Önállóan álló tőszámneveket (pl. "1234") szavakká alakít (pl. "ezerkétszázharmincnégy").
10. **Nem Kívánt Karakterek Eltávolítása (`remove_unwanted_characters`):** Eltávolít egy előre definiált speciális karakterkészletet (pl. `*`, `"`, `(`, `)`) úgy, hogy szóközökkel helyettesíti őket.
11. **Specifikus Kötőjeles Szavak Kezelése:** Kezeli az olyan specifikus kötőjeles mintákat, mint "egy-egy", átalakítva azokat "egy egy"-re.
12. **Kötőjelek Eltávolítása:** Eltávolítja a megmaradt kötőjeleket az összekapcsolt részek egyesítésével.
13. **Többszörös Szóközök Eltávolítása (`remove_duplicate_spaces`):** Összevonja a többszörös szóközöket egyetlen szóközzé, és eltávolítja a szöveg elejéről/végéről a felesleges szóközöket.
14. **Előtag Hozzáadása (`add_prefix`):** Hozzáadja a "... " előtagot a feldolgozott szöveg elejéhez.
15. **Kisbetűssé Alakítás (`convert_to_lowercase`):** Az egész szöveget kisbetűssé alakítja.

## Konfigurációs Fájlok

A normalizálási folyamat testreszabható két CSV fájl segítségével: `changes.csv` és `force_changes.csv`. Ezeknek a fájloknak ugyanabban a könyvtárban kell lenniük, mint a `normaliser.py`.

### `changes.csv`

Ez a fájl általános, teljes szavas cserékhez használatos. A CSV fájl minden sora két, vesszővel elválasztott értéket kell, hogy tartalmazzon:

*   **Kulcs:** A lecserélendő szó vagy kifejezés. Az illesztés nem különbözteti meg a kis- és nagybetűket, és csak teljes szavakra vonatkozik.
*   **Érték:** A sztring, amely lecseréli a kulcsot.

**Példa `changes.csv` bejegyzésre:**

```csv
AI,mesterséges intelligencia
GPU,grafikus processzor
like,lájk
```

Ebben a példában minden "AI" egész szavas előfordulás (kis- és nagybetűtől függetlenül) "mesterséges intelligencia"-ra lesz cserélve.

### `force_changes.csv`

Ez a fájl specifikusabb és "erőteljesebb" rész-sztring cseréket tesz lehetővé. Képes szavak részeit lecserélni, és szabályozni tudja a kicserélt érték körüli szóközöket. A CSV fájl minden sora négy, vesszővel elválasztott értéket kell, hogy tartalmazzon:

*   **Kulcs:** A pontosan lecserélendő sztring. Az illesztés megkülönbözteti a kis- és nagybetűket, és a szöveg bármely részén előfordulhat (azaz rész-sztring egyezés).
*   **Érték:** A sztring, amely lecseréli a kulcsot.
*   **Szóközök Előtte:** Egy egész szám, amely meghatározza, hogy hány szóköz kerüljön az `Érték` elé a csere után.
*   **Szóközök Utána:** Egy egész szám, amely meghatározza, hogy hány szóköz kerüljön az `Érték` után a csere után.

**Példa `force_changes.csv` bejegyzésre:**

```csv
ninjutsu,nindzsucu,0,0
chips,csipsz,0,0
% , százalék ,0,0
```

Ebben a példában:
*   A "ninjutsu" "nindzsucu"-ra lesz cserélve, hozzáadott szóközök nélkül.
*   A "chips" "csipsz"-re lesz cserélve, hozzáadott szóközök nélkül.
*   A "% " " százalék "-ra lesz cserélve (figyeljük meg a szóközöket magában az értékben, ha szükséges, vagy a két utolsó oszlop által szabályozva).

**Megjegyzés:** A `force_changes.csv` szabályai a legtöbb egyéb normalizálási lépés *előtt* kerülnek alkalmazásra, beleértve a `changes.csv`-t, a mozaikszavak kezelését és a számok átalakítását. Ez lehetővé teszi számukra, hogy megelőzzenek vagy előkészítsenek szövegrészeket a későbbi szabályok számára.

## Használat

A normalizáló használatához importálja a `normalize` függvényt a `normaliser.py` szkriptből, és adja át neki a magyar szöveget.

**Python Példa:**

```python
from normaliser import normalize

text_to_normalize = "A NATO IV. közgyűlése 2024. máj. 1-jén lesz 10:00-kor. Ez egy v2 API."
normalized_text = normalize(text_to_normalize)
print(f"Eredeti: {text_to_normalize}")
print(f"Normalizált: {normalized_text}")

# Várható kimenet (az időformázásban lévő véletlenszerű választások miatt kissé eltérhet):
# Eredeti: A NATO IV. közgyűlése 2024. máj. 1-jén lesz 10:00-kor. Ez egy v2 API.
# Normalizált: ... a en á té ó negyedik közgyűlése kétezerhuszonnégy május elsején lesz tíz órakor ez egy vé kettő á pé í
```

Győződjön meg róla, hogy a `normaliser.py`, `changes.csv`, és `force_changes.csv` fájlok ugyanabban a könyvtárban vannak, vagy módosítsa a fájlútvonalakat a `changes.csv` és `force_changes.csv` betöltéséhez a `normaliser.py` szkripten belül, ha máshol helyezkednek el. A szkript jelenleg úgy van beállítva, hogy ezeket a CSV fájlokat a saját könyvtárában keresse.

## Tesztelés

A repository tartalmaz egy tesztszkriptet, `normalizer_test.py`, amely különböző teszteseteket tartalmaz a normalizáló funkcionalitásának bemutatására és ellenőrzésére.

A tesztek futtatásához hajtsa végre a szkriptet a terminálból:

```bash
python normalizer_test.py
```

Ez kiírja több mintaszöveg eredeti és normalizált változatát, lehetővé téve a különböző normalizálási szabályok viselkedésének vizsgálatát.

## Függőségek

A szkript a következő Python csomagra támaszkodik:

*   **num2words:** Számok (tő- és sorszámnevek) magyar szavas megfelelőjévé alakítására használatos.

Telepítheti pip segítségével:

```bash
pip install num2words
```
