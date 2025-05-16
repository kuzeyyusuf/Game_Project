#   Chimp Test Battle Game

Bu proje, **Pygame** ile geliştirilmiş hafızaya dayalı bir mini oyunudur. Oyuncular sırasıyla **chimp testine dayalı hafıza kutularına** tıklayarak karşı tarafa hasar verir. Oyun; müzik, animasyonlar, sesler ve karakter saldırı animasyonları içerir.

## Özellikler

-  Arka planda çalan  müzik listesi Witcher 3 Gwent Müzikleri)
-  Mage ve Knight karakterleri
-  Zar atışına dayalı saldırı sistemi
-  Flüt, gitar, davul gibi müzik enstrümanı animasyonları
-  Hafıza testi (chimp grid sistemi)
-  Turlar ve oyuncu sırası gösterimi
-  Can sistemi ve oyun sonu koşulları

##  Gereksinimler

- Python 3.x
- `pygame` kütüphanesi

Kurulum için:

```bash
pip install pygame
```

## Nasıl Oynanır?

- `Enter` tuşuna basarak sıranı başlat.
- Gösterilen kutuların sırasını aklında tut ve doğru sırayla tıkla.
- Hatalı tıklarsan zar atışıyla hasar verme şansı doğar.
- Saldırılar karakter animasyonlarıyla birlikte gerçekleşir.
- Flüt, gitar, davul gibi animasyonlar dekoratif olarak sahnede döner.
- Oyunculardan birinin canı sıfırlanırsa oyun biter (`R` tuşu ile tekrar başlatılabilir).

## 🎵 Müzik Sistemi

- `Assets/Music/` klasöründe bulunan şarkılar otomatik olarak sırayla çalınır.
- Playlist döngülüdür, her şarkı bittikçe sıradaki otomatik başlar.

## 🔧 Klasör Yapısı

```
project/
├── main.py
├── README.md
├── Assets/
│   ├── Music/
│   │   ├── track1.mp3
│   │   ├── flute_0.png ... flute_15.png
│   │   ├── guitar_0.png ... guitar_50.png
│   │   └── drums_0.png ... drums_15.png
│   ├── Sprites/
│   │   ├── Idle.png
│   │   ├── Attack.png
│   │   └── ...
│   ├── background_layer_1.png
│   ├── ...
```


##  Lisans

Bu proje kişisel eğitim amaçlıdır. Müzik ve sprite dosyaları telifli olabilir.
