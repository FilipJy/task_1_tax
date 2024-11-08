# Aplikace pro výpočet daně (úkol)

Tato aplikace umožňuje vypočítat daň pro pozemky a stavby. Součástí je také registr majitelů umožňující uložit a spravovat informace o majiteli a jejich majetku.

# Instalace a spuštění aplikace

## Instalace

Tato aplikace využívá pouze defaultní python balíčky, není tedy třeba žádné instalovat. Stačí tedy stáhnout/ clone main branch.

`git clone https://github.com/FilipJy/task_1_tax.git`

## Spuštění

V terminálu kořenu složky:

python main.py

# Použití aplikace

Aplikace se skládá ze dvou základních funkcí - výpočet daně (tax) a registr majitelů (registr)

## Tax (výpočet daně)

Po volbě možnosti **"tax"** lze zvolit jaký druh daně spočítat. Základní možnosti jsou **"pozemek"** pro výpočet daně pozemku, a **"stavba"** pro výpočet daně budov. Po volbě jedné z těchto možností je uživatel vyzván k zadání základních informaci pro výpočet daně. Po výpočtu má uživatel možnost uložit a přiřadit majetek i s výpočtem k majiteli z registru. Tato možnost předpokládá, že majitel již v registru existuje.

Další možnost je **"hromadně"**, pro sečtení všech pozemků a staveb zvoleného majitele. Tato možnost opět předpokládá, že je majitel zapsán v registru.

## Registr (registr majitelů a majetku)

Po volbě možnosti **"registr"** se uživatel dostane do registru majitelů a majetku. Zde lze:

 ### zapsat nového majitele (**"nový"**):
 Uživatel je vyzván zadat základní informace o novém majiteli. Po úspěšném uložení majitele je pro záznam vygenerováno unikátní ID, sloužící k identifikaci majitele.

 ### vypsat již existující majitele (**"výpis"**):
 Majitele lze vypsat buď jednotlivě, a to pomocí ID, nebo hromadně.
 V případě výpisu záznamu konkrétního majitele bude vypsán i majetek, který byl majiteli přidělen.

 ### upravit již existující záznam (**"úprava"**)
 Uživatel je nejprve vyzván k volbě majitele pomocí ID. Poté může upravit jednotlivé informace. Pro zachování původní hodnoty lze pole nechat prázdné.

 ### smazat majitele (**"smazat"**)
Pomocí této možnosti lze smazat majitele (a přiřazený majetek) z registru. Uživatel je nejprve vyzván identifikovat majitele pomocí ID.
 
 
 
 
