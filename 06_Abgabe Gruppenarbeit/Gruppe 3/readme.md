# 1_Rohdaten
Dieser Ordner enthält alle Roh-Files, die aus dem Scraping entstanden sind
## Alle_Aktionsweine.csv <br />
Ist die Liste aller Weine, die zum Scrape-Zeitpunkt bei Coop in Aktion waren
## Rotweine_1.csv und Rotweine_2.csv <br />
Enthalten je ein Subset aller Rotweine, die von Coop gescraped wurden
## Weissweine_1.csv und Weissweine_2.csv <br />
Enthalten je ein Subset aller Weissweine, die von Coop gescraped wurden
# Finaler Datensatz
## Alle_Weine_v5.xlsx <br />
Enthält den Datensatz, so wie er nach der Bereinigung aller Daten final erstellt worden ist und für die weitere Bearbeitung wie das Interface oder Tableau verwendet wurde.
# interface
## 240506_All_Wines_formatted_v6.csv <br />
Beinhaltet das finale file als csv, damit es für die für das Interface zur Verfügung steht.
## interface.py <br />
Ist der Python-Code, mit dem das Interface codiert wurde. Das Interface sollte über den Terminal ausgeführt werden. Hierbei sollte man zum Ordner, in welchem die Datei gespeichert ist navigieren und dann "streamlit run interface.py" ausführen um das Interface zu starten. Das Interface wird dann lokal ausgeführt und kann im Browser gesehen werden. Wichtig ist, dass sowohl Streamlit als auch pandas installiert sind vor der Ausführung. 
## MainScraper.py <br />
Python Programm code, der das Scraping der Daten von Coop und Vivino orchestriert
## Robert Parker Guide Originales PDF.pdf <br />
Heruntergeladenes PDF von Robert Parker. Enthalt die Ratings von Weinregionen pro Jahr.
## Robert Parker Guide_Bereinigt.xlsx <br />
Enthält die bereinigten Daten in Excel-Format aus dem Robert Parker Guide.
## Wineguide_Graphics.twb <br />
Tableau-File mit allen erstellten Analysesheets, Dashboards und Visuals-Story
## coopScraper.py <br />
Python Code, der für das crawlen der Coop-Webseite zuständig ist.
## vivinoScraper.py <br />
Python Code, der für das crawlen der Vivino-Webseite zuständig ist.
