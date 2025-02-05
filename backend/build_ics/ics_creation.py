import uuid
from datetime import datetime, timedelta
import pytz
from pathlib import Path
from build_ics.scraping import get_spiele_infos

MANNSCHAFTEN = {
    "DJK_I": "https://www.bfv.de/partial/mannschaftsprofil/spielplan/016PALNC9K000000VV0AG80NVV8OQVTB/naechste?wettbewerbsart=1&spieltyp=ALLE&from=10&size=10",
    "DJK_II": "https://www.bfv.de/partial/mannschaftsprofil/spielplan/016PK3R8NC000000VV0AG80NVUT1FLRU/naechste?wettbewerbsart=1&spieltyp=ALLE&from=10&size=10",
}

icalendar_header = """BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//DJK//DE\r
CALSCALE:GREGORIAN\r
BEGIN:VTIMEZONE\r
TZID:Europe/Berlin\r
X-LIC-LOCATION:Europe/Berlin\r
BEGIN:DAYLIGHT\r
TZOFFSETFROM:+0100\r
TZOFFSETTO:+0200\r
TZNAME:CEST\r
DTSTART:19700329T020000\r
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\r
END:DAYLIGHT\r
BEGIN:STANDARD\r
TZOFFSETFROM:+0200\r
TZOFFSETTO:+0100\r
TZNAME:CET\r
DTSTART:19701025T030000\r
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\r
END:STANDARD\r
END:VTIMEZONE\r
"""

ZEITZONE = pytz.timezone("Europe/Berlin")

def create_ics(team: str):
    url = MANNSCHAFTEN[team]
    spiele: list[dict] = get_spiele_infos(url)

    # Start building the calendar file with the header
    icalendar_content = icalendar_header
    
    for spiel in spiele:
        uid = str(uuid.uuid4())  # Generate a random UID
        
        # Parse the date and time
        datum_zeit = ZEITZONE.localize(
            datetime.strptime(f"{spiel['datum']} {spiel['uhrzeit']}", '%d.%m.%Y %H:%M Uhr')
        )
        start = datum_zeit.strftime('%Y%m%dT%H%M%S')
        end = (datum_zeit + timedelta(hours=3)).strftime('%Y%m%dT%H%M%S')

        Gegner = spiel["team0"] if "Ottenhofen" not in spiel["team0"] else spiel["team1"]
        summary = f"Spiel gegen {Gegner}"
        
        # Add the event to the calendar content
        icalendar_content += (
            "BEGIN:VEVENT\r\n"
            f"UID:{uid}\r\n"
            f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}\r\n"
            f"DTSTART;TZID=Europe/Berlin:{start}\r\n"
            f"DTEND;TZID=Europe/Berlin:{end}\r\n"
            f"SUMMARY:{summary}\r\n"
            f"LOCATION:{spiel['adresse']}\r\n"
            f"DESCRIPTION:{spiel['team0']} vs. {spiel['team1']}.\r\n"
            "SEQUENCE:0\r\n"
            "CATEGORIES:Sport\r\n"
            "END:VEVENT\r\n"
        )

    # Close the calendar
    icalendar_content += "END:VCALENDAR\r\n"

    # Save the single ics file for the team
    folder_path = Path(f"djk-kalender-app/src/spieltermine")
    folder_path.mkdir(parents=True, exist_ok=True)

    ics_file_path = folder_path / f"{team}_alle_spiele.ics"
    with open(ics_file_path, "w") as ics_file:
        ics_file.write(icalendar_content)
        
        
if __name__ == "__main__":
    create_ics("DJK_I")
    create_ics("DJK_II")
    print("ICS files created successfully.")
