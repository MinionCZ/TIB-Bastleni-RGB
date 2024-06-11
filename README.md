# TIB RGB Pásek

Tento repozitář slouží pro uchování firmware v Micropythonu pro kroužek bastlení s rodiči pro projekt řadiče pro RGB LED
pásek. Kód v sobě obsahuje komentáře pro lepší pochopení.

## Nahrání firmware z PyCharm

Než se pustíme do nahrávání firmwaru do našeho zařízení, tak je potřeba připravit PyCharm pro práci s MicroPythonem.

### Přidání a nastavení MicroPython pluginu

1. Otevřeme si nastavení (settings) a v něm si najdeme podsložku plugins
2. V plugins klikneme na marketplace a do vyhledávacího okna napíšeme MicroPython
3. Klikneme na plugin a dáme ho
   nainstalovat ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/8f52a090-c945-40fa-9f99-5f4f0e255fcf)
4. Nejspíše bude potřeba po instalaci potřeba restartovat PyCharm, tak ho prosím restartujte
5. Po restartování si otevřeme opět nastavení a v levém horním rohu do vyhledávacího pole napíšeme MicroPython
6. Pod záložkou Languages&Frameworks bychom měli vidět Micropython. Klikneme na položku
7. V okně zaklikneme, že chceme mít podporu MicroPythonu a vybereme zařízení RaspberryPi Pico z nabídky
8. Poté ještě zaškrtneme, že si port má najít
   sám ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/fc059aea-8972-4918-9120-11115aab58f7)
9. Nastavení uložíme kliknutím na OK

Detailnější návod pro přidání pluginu a představení pluginu lze
najít [zde](https://medium.com/@andymule/micropython-in-pycharms-basic-setup-9169b497ec8a).

## Nahrání firmware

1. Nejprve je potřeba označit adresář/složku src jako sources root (kořen zdrojových
   souborů) ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/87420fcf-56ee-4e76-ad6b-58450977a68f)
2. Dále je potřeba si vytvořit novou configuraci
   nahrání ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/4dc1c87f-9ac3-4768-81c3-d247e48352e4)
3. Tím se nám otevře dialogové okne, kde klikneme
   na + ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/a505c6e9-b0c4-4e8b-837a-9d2fb8faec7a)
4. Zde vybereme MicroPython a
   klikneme ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/6b1a7d5c-0735-4e97-96c0-6952baa42c35)
5. Poté zvolíme cestu k našemu zdrojovému kódu tím, že klikneme na tlačítko složky u vstupního pole
   Path ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/06cc0e5b-4d01-4937-aa91-d53d2bfa064b) ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/88360cbc-0f28-4b5a-802e-e22ca6e0919c)
6. Cestu potvrdíme klikem na ok
7. Nyní bychom měli vidět nastavenou
   konfiguraci ![image](https://github.com/MinionCZ/TIB-Bastleni-RGB/assets/43399650/d3010626-3632-4f9e-a92a-7d186235aa6b)
8. Nyní by nám měl jít nahrát firmware pomocí zelené šipky vedle konfigurace
