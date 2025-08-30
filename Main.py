from Functions_Scraping import *
import warnings

links_file = r"C:\Users\rodmo\Desktop\MBD Maestría EGADE\Gestión de Bases de Datos y Computación en la Nube\Archivo Local Laptop Gestión de Bases de Datos y Computación en la Nube\Link Twitter Scraping.xlsx"
links, status = get_links(links_file)

links = links[:15]  # Limit to first 10 links for testing
status = status[:15]  # Limit to first 10 statuses for testing



time1 = time.time()
twits, fechas, plataformas, links_scraped, status_id, status_id_parent = scrape_twitter(links, status, count=0)
time2 = time.time()
timedelta = round(time2 - time1,0)
print(f"Scraping completed in {timedelta} seconds")


df = pd.DataFrame({
    'Twit': twits,
    'Fecha': fechas,
    'Plataforma': plataformas,
    'Status ID': status_id,
    'Status ID Parent': status_id_parent,
    'Link': links_scraped
    })

excel_file = r"C:\Users\Usuario\Desktop\Personal\Maestría MBD\Gestión de Bases de Datos y Computación en la Nube\Twitter Scraping Results.xlsx"
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Twitter Scraping DB', index=False)
    
print(f"Data successfully saved to {excel_file}")
