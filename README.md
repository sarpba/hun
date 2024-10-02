Egyelőre fejlesztés alatt, lehet lesz belőle valami idővel, de lehet hogy nem :) (Még határozottan nincs kész!! Ha van ötleted írd meg.)

Letöltés:
```
wget https://raw.githubusercontent.com/sarpba/huntextnormaliser/main/huntextnormaliser.py
```

Használat:
```
import importlib
import huntextnormaliser
importlib.reload(huntextnormaliser)
from huntextnormaliser import HungarianTextNormalizer

normalizer = HungarianTextNormalizer()
sample_text = "Az időpont 13h:15m:45s volt."
normalized_text = normalizer.normalize(sample_text)
print(normalized_text)
```

A kimenete ez kell legyen:
```
Az időpont tizenhárom óra tizenöt perc negyvenöt másodperc volt.
```
