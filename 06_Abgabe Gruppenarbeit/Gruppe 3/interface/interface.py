# Beschreibung: Dieses Skript dient dazu, die Weine zu filtern und in einem Interface anzuzeigen. Das Dashboard ist
# unabhängig vom Scraping-Prozess selbst und kann auch ohne diesen ausgeführt werden so lange die benötigten Daten
# geliefert werden. Das Dashboard ermöglicht es dem Benutzer, die Weine nach verschiedenen Kriterien zu filtern, wie
# z.B. Preis, Land, Geschmacksprofil, etc. und zeigt dann die entsprechenden Weine an.

# Hier werden Pandas & Streamlit importiert. Pandas nutzen wir für das Einlesen und manipulieren der Daten. Streamlit
# ist ein Framework, das es ermöglicht, Web-Apps zu erstellen und für die Visualisierung unserer Daten gut geeignet
# ist. Wir haben uns für Streamlit entschieden, da es relativ simpel und auch gut aussieht im Vergleich zu anderen
# Frameworks, welche wir ausprobiert haben.
import pandas as pd
import streamlit as st

# Funktion zum Sicherstellen, dass die eingelesenen Daten einheitlich sind. Hierbei werden z.B. die Spalten 'Preis'
# und die Geschmacksprofile in numerische Werte umgewandelt. Auch werden die Jahre als String gespeichert,
# da sie ansonsten mit Tausender-Strichen in der Tabelle angezeigt werden, was unübersichtlich ist.
# Zuletzt wird noch die Reihenfolge der Spalten festgelegt.
def load_data(path):
    wines = pd.read_csv(path)
    wines['Preis'] = pd.to_numeric(wines['Preis'], errors='coerce')
    wines = wines.dropna(axis=1, how='all')
    wines['Trocken / Süss'] = wines['Trocken / Süss'].replace('0]', '0')
    wines['Leicht / Üppig'] = wines['Leicht / Üppig'].astype('float64')
    wines['Sanft / Tanninhaltig'] = wines['Sanft / Tanninhaltig'].astype('float64')
    wines['Trocken / Süss'] = wines['Trocken / Süss'].astype('float64')
    wines['Weich / Säurehaltig'] = wines['Weich / Säurehaltig'].astype('float64')
    wines['Jahr'] = wines['Jahr'].astype(str)
    desired_order = [
        'Name', 'Land', 'Jahr', 'Preis', 'Bewertung', 'Robert Parker', 'Anzahl Bewertungen',
        'In Aktion', 'Farbe', 'Leicht / Üppig', 'Sanft / Tanninhaltig', 'Trocken / Süss', 'Weich / Säurehaltig'
    ]
    wines = wines[desired_order]
    return wines


# Funktion zum Verteilen der Geschmacksprofile auf die entsprechenden Spalten Sie wurde genutzt, um die gescrapeten
# Rohdaten in ein einheitliches Format zu bringen, wird  aber jetzt nicht mehr genutzt.
def distribute_tastes(df):
    tastes = df['Tastes']
    if tastes is not None:
        if len(tastes) == 4:
            df['Leicht / Üppig'], df['Sanft / Tanninhaltig'], df['Trocken / Süss'], df['Weich / Säurehaltig'] = tastes
        elif len(tastes) == 3:
            df['Leicht / Üppig'], df['Trocken / Süss'], df['Weich / Säurehaltig'] = tastes[0], tastes[1], tastes[2]
    return df


# Funktion zum Erstellen einer Liste aller Länder, in denen Weine verkauft werden. Die Länder werden alphabetisch
# geordnet.
def get_unique_countries(all_wines):
    countries = all_wines['Land'].dropna().unique()
    countries = sorted(countries)
    countries.insert(0, 'Alle Länder')
    return countries


# Diese Funktion filtert die Weine nach den vom Benutzer eingegebenen Kriterien. Hierbei wird der Preis, das Land,
# die Art des Weines, und das Geschmacksprofil in betracht gezogen.
def filter_wines(wines, price_min, price_max, selected_country, wine_type, selected_light_bold, selected_smooth_tannic,
                 selected_dry_sweet, selected_soft_acidic):
    filtered = wines[(wines['Preis'] >= price_min) & (wines['Preis'] <= price_max)]
    if selected_country != 'Alle Länder':
        filtered = filtered[filtered['Land'] == selected_country]
    if wine_type != 'Beides':
        filtered = filtered[filtered['Farbe'] == ('R' if wine_type == 'Rot' else 'W')]
    if selected_light_bold != 'Indifferent':
        filtered = filtered[filtered['Leicht / Üppig'] == selected_light_bold]
    if selected_smooth_tannic != 'Indifferent':
        filtered = filtered[filtered['Sanft / Tanninhaltig'] == selected_smooth_tannic]
    if selected_dry_sweet != 'Indifferent':
        filtered = filtered[filtered['Trocken / Süss'] == selected_dry_sweet]
    if selected_soft_acidic != 'Indifferent':
        filtered = filtered[filtered['Weich / Säurehaltig'] == selected_soft_acidic]
    return filtered


# Funktionen zum Kategorisieren der Geschmacksprofile. Hier werden Prozentangaben einfachheitshalber in drei
# Kategorien unterteilt. Wir wollten dies so, um die Bedienung und Verständlichkeit für nicht-Weinkenner zu
# vereinfachen. Diese wurden für jeden der 4 Geschmäcker erstellt.
def categorize_light_bold(taste_value):
    if 0 <= taste_value < 40:
        return 'Leicht'
    elif 40 <= taste_value <= 60:
        return 'Ausgewogen'
    elif 60 < taste_value <= 100:
        return 'Üppig'
    else:
        return None


def categorize_smooth_tannic(taste_value):
    if 0 <= taste_value < 40:
        return 'Sanft'
    elif 40 <= taste_value <= 60:
        return 'Ausgewogen'
    elif 60 < taste_value <= 100:
        return 'Tanninhaltig'
    else:
        return None


def categorize_dry_sweet(taste_value):
    if 0 <= taste_value < 40:
        return 'Trocken'
    elif 40 <= taste_value <= 60:
        return 'Ausgewogen'
    elif 60 < taste_value <= 100:
        return 'Süss'
    else:
        return None


def categorize_soft_acidic(taste_value):
    if 0 <= taste_value < 40:
        return 'Weich'
    elif 40 <= taste_value <= 60:
        return 'Ausgewogen'
    elif 60 < taste_value <= 100:
        return 'Säurehaltig'
    else:
        return None


# Hier noch einen Dictionary mit den deutschen Übersetzungen für die Texte, die auf der Webseite angezeigt werden.
# Dies war, weil anfangs das Dashboard auf English geschrieben wurde, wir uns aber dann umentschieden haben es auf
# Deutsch darzustellen.
translations = {
    'Wine Selection Dashboard': 'Wein Auswahl Dashboard',
    'Discover the best rated wines that match your preferences.': 'Entdecke die am besten Bewerteten Weine die deinen Präferenzen entsprechen.',
    'Preferences': 'Präferenzen',
    'Choice of wine type': 'Wahl des Wein Typs',
    'Red': 'Rot',
    'White': 'Weiss',
    'Both': 'Beides',
    'Minimum price': 'Minimaler Preis',
    'Maximum price': 'Maximaler Preis',
    'Select a country': 'Land auswählen',
    'All countries': 'Alle Länder',
    'Light-Bold': 'Leicht / Üppig',
    'Smooth-Tannic': 'Sanft / Tanninhaltig',
    'Dry-Sweet': 'Trocken / Süss',
    'Soft-Acidic': 'Weich / Säurehaltig',
    'Indifferent': 'Indifferent',
    'The best wines from': 'Die besten Weine von',
    'No wines found with the given criteria.': 'Keine Weine mit den vorgegebenen Kriterien gefunden.',
    'Show more': 'Mehr anzeigen',
    'Show less': 'Weniger anzeigen'
}

# Hier wird das Dashboard erstellt. Es wird ein Titel und eine Beschreibung hinzugefügt. Zudem wird die Breite des
# Dashboards definiert.
st.set_page_config(layout="wide")
st.title(translations['Wine Selection Dashboard'])
st.write(translations['Discover the best rated wines that match your preferences.'])

# Hier wird der Session State initialisiert. Dieser wird genutzt, um die Eingaben des Benutzers zu speichern,
# insbesondere beim filtern ist der Session State sehr hilfreich.
if 'init' not in st.session_state:
    st.session_state['show_more'] = False
    st.session_state['wine_type'] = translations['Both']
    st.session_state['price_min'] = 10
    st.session_state['price_max'] = 50
    st.session_state['selected_country'] = 'Alle Länder'
    st.session_state['selected_light_bold'] = 'Indifferent'
    st.session_state['selected_smooth_tannic'] = 'Indifferent'
    st.session_state['selected_dry_sweet'] = 'Indifferent'
    st.session_state['selected_soft_acidic'] = 'Indifferent'
    st.session_state['min_reviews'] = False
    st.session_state['in_aktion'] = False
    st.session_state['init'] = True

# Hier wird der Knopf zum Anzeigen von mehr Weinen initialisiert. Dieser wird genutzt, um die Anzahl der angezeigten
# Weine zu erhöhen oder zu verringern.
if 'show_more' not in st.session_state:
    st.session_state['show_more'] = False

# Nun werden die Daten eingelesen und die Länder in einer Liste gespeichert.
all_wines = load_data("240506_All_Wines_formatted_v6.csv")
countries = get_unique_countries(all_wines)

# Hier werden die Geschmacksprofile kategorisiert.
categorized_wines = all_wines.copy()
categorized_wines['Leicht / Üppig'] = categorized_wines['Leicht / Üppig'].apply(categorize_light_bold)
categorized_wines['Sanft / Tanninhaltig'] = categorized_wines['Sanft / Tanninhaltig'].apply(categorize_smooth_tannic)
categorized_wines['Trocken / Süss'] = categorized_wines['Trocken / Süss'].apply(categorize_dry_sweet)
categorized_wines['Weich / Säurehaltig'] = categorized_wines['Weich / Säurehaltig'].apply(categorize_soft_acidic)

filtered_wines = categorized_wines.copy()

# Initialisierung der Sidebar und der Filtermöglichkeiten
st.sidebar.header(translations['Preferences'])
wine_type_options = (translations['Red'], translations['White'], translations['Both'])
st.session_state['wine_type'] = st.sidebar.selectbox(translations['Choice of wine type'], wine_type_options, index=wine_type_options.index(st.session_state.get('wine_type', translations['Both'])))
st.session_state['price_min'] = st.sidebar.number_input(translations['Minimum price'], min_value=0, value=st.session_state.get('price_min', 10))
st.session_state['price_max'] = st.sidebar.number_input(translations['Maximum price'], min_value=0, value=st.session_state.get('price_max', 50))

# Kleiner Check, ob der minimale Preis nicht den maximalen Preis übersteigt.
if st.session_state['price_min'] > st.session_state['price_max']:
    st.sidebar.error('Minimaler Preis darf nicht den Maximalen Preis übersteigen.')

# Restlichen Filtermöglichkeiten
st.session_state['selected_country'] = st.sidebar.selectbox(translations['Select a country'], countries, index=countries.index(st.session_state.get('selected_country', 'Alle Länder')))
st.session_state['selected_light_bold'] = st.sidebar.selectbox('Leicht / Üppig', ('Indifferent', 'Leicht', 'Ausgewogen', 'Üppig'), index=['Indifferent', 'Leicht', 'Ausgewogen', 'Üppig'].index(st.session_state.get('selected_light_bold', 'Indifferent')))
st.session_state['selected_smooth_tannic'] = st.sidebar.selectbox('Sanft / Tanninhaltig', ('Indifferent', 'Sanft', 'Ausgewogen', 'Tanninhaltig'), index=['Indifferent', 'Sanft', 'Ausgewogen', 'Tanninhaltig'].index(st.session_state.get('selected_smooth_tannic', 'Indifferent')))
st.session_state['selected_dry_sweet'] = st.sidebar.selectbox('Trocken / Süss', ('Indifferent', 'Trocken', 'Ausgewogen', 'Süss'), index=['Indifferent', 'Trocken', 'Ausgewogen', 'Süss'].index(st.session_state.get('selected_dry_sweet', 'Indifferent')))
st.session_state['selected_soft_acidic'] = st.sidebar.selectbox('Weich / Säurehaltig', ('Indifferent', 'Weich', 'Ausgewogen', 'Säurehaltig'), index=['Indifferent', 'Weich', 'Ausgewogen', 'Säurehaltig'].index(st.session_state.get('selected_soft_acidic', 'Indifferent')))

# Diese Filtermöglichkeiten sind noch speziell, da diese Checkboxen sind. Diesen wird auch noch ein "key" gegeben,
# um sie klar auseinander zu halten.
st.session_state['min_reviews'] = st.sidebar.checkbox('Mindestens 1000 Bewertungen', value=st.session_state.get('min_reviews', False), key='min_reviews_key')
st.session_state['in_aktion'] = st.sidebar.checkbox('In Aktion', value=st.session_state.get('in_aktion', False), key='in_aktion_key')

# Hier werden die Weine gefiltert, basierend auf den vom Benutzer angegebenen  Kriterien.
filtered_wines = filter_wines(
    categorized_wines,
    st.session_state['price_min'],
    st.session_state['price_max'],
    st.session_state['selected_country'],
    st.session_state['wine_type'],
    st.session_state['selected_light_bold'],
    st.session_state['selected_smooth_tannic'],
    st.session_state['selected_dry_sweet'],
    st.session_state['selected_soft_acidic']
)

# Aktionen, wenn die Checkboxen ausgewählt werden.
if st.session_state['min_reviews']:
    filtered_wines = filtered_wines[categorized_wines['Anzahl Bewertungen'] >= 1000]

if st.session_state['in_aktion']:
    filtered_wines = filtered_wines[categorized_wines['In Aktion'] == 1]

# Reset-Knopf der alle Filter wieder rausnimmt
if st.sidebar.button('Filter Zurücksetzen'):
    # Reset all filters to their default values
    st.session_state['show_more'] = False
    st.session_state['wine_type'] = translations['Both']
    st.session_state['price_min'] = 10
    st.session_state['price_max'] = 50
    st.session_state['selected_country'] = 'Alle Länder'
    st.session_state['selected_light_bold'] = 'Indifferent'
    st.session_state['selected_smooth_tannic'] = 'Indifferent'
    st.session_state['selected_dry_sweet'] = 'Indifferent'
    st.session_state['selected_soft_acidic'] = 'Indifferent'
    st.session_state['min_reviews'] = False
    st.session_state['in_aktion'] = False
    st.rerun()

# Nun wird das Dataframe angezeigt, welches die gefilterten Weine enthält. Es wird auch noch formatiert, damit es
# übersichtlicher ist.
if not filtered_wines.empty:
    st.write(f"{translations['The best wines from']} ({st.session_state['price_min']} bis {st.session_state['price_max']} CHF):")
    num_wines_to_show = len(filtered_wines) if st.session_state['show_more'] else 10

    # Prepare the dataframe for display
    display_wines = filtered_wines.sort_values(by='Bewertung', ascending=False).head(num_wines_to_show)
    display_wines = display_wines.reset_index(drop=True)
    display_wines.index += 1  # Start index at 1

    st.dataframe(
        display_wines.style.format({'Preis': "{:.2f}", 'Bewertung': "{:.1f}", 'Anzahl Bewertungen': "{:,.0f}"}, thousands="'"), width=1800)

    if st.button('Mehr anzeigen' if not st.session_state['show_more'] else 'Weniger anzeigen', key="show_more_button"):
        st.session_state['show_more'] = not st.session_state['show_more']
        st.rerun()
# Falls die Filter zu keinem Ergebnis führen, wird eine entsprechende Meldung angezeigt.
else:
    st.write(translations['No wines found with the given criteria.'])


