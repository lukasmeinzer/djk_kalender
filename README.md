# djk_kalender
Automatisiert Kalendereinträge der DJK Spiele erstellen.
Abrufbar unter https://djk-ottenhofen-kalender.de/


## Anleitung

Zwei mal im Jahr (zur neuen Rück- bzw. Hinrunde) muss die .ics-Datei Erstellung manuell angetriggert werden

Hierfür:
- gehe auf die BFV Website der DJK: https://www.bfv.de/vereine/djk-sp-gschft-ottenhofen/00ES8GNHEC000010VV0AG08LVUPGND5I
- Wähle die DJK Herren I
- Rechtsklick -> Untersuchen
- Wechsle auf den Reiter "Network" und wähle "Fetch/XHR"
- Scrolle auf der Website nach unten zu den Spielen und klicke solange auf "MEHR ANZEIGEN", bis alle Spiele sichtbar sind
- Wähle auf der rechten Seite den letzten Eintrag, der mit "naechste\" beginnt
- kopiere die Request URL im Headers-Reiter
- Öffne VSCode und öffne die Datei create_ics/main.py
- Ersetze hier die URL im MANNSCHAFTEN dictionary für DJK_I

--> Wiederhole den Vorgang für DJK_II

- Sobald alle URLs in MANNSCHAFTEN ersetzt sind, führe das Python Skript aus
- Alle Ergebnisse werden in den Ordnern spieltermine_* gespeichert
- Prüfe die Ergebnisse stichprobenhaft, indem du die .ics-Datei herunterlädst und hier https://icalendar.org/validator.html überprüfst
- Außerdem: schicke dir einzelne .ics Dateien selbst per Mail und prüfe, ob du sie richtig in deinen Kalender eintragen kannst
