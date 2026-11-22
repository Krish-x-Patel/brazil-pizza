#!/usr/bin/env python3
"""Builds index.html for Brazil Pizza from one menu list, so prices only live in one place.

To change a price or dish: edit MENU below, then run `python3 tools/build.py` from the repo folder.
Prices come from the restaurant's own online ordering page (Square). A price like "23.90-31.90"
is a range by size.
"""
import html, os

ORDER = "https://orderbrazilpizza.square.site/"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=Brazil+Pizza+279+Powers+Ferry+Rd+SE+Ste+B+Marietta+GA+30067"
EMBED = "https://www.google.com/maps?q=Brazil+Pizza,+279+Powers+Ferry+Rd+SE,+Marietta,+GA+30067&output=embed"
TEL = "tel:+14044211426"
INSTA = "https://www.instagram.com/brazilpizzamarietta/"

# group id, group title, note, items: (name, portuguese, price, description, image or None)
MENU = [
 ("deal", "Tuesday to Thursday deal", "", [
  ("Classic pizza combo", "", "29.90", "Large pizza, garlic or pepperoni bread, and a 2-liter soda", None),
 ]),
 ("savory", "Savory pizzas", "Pizza inteira salgada", [
  ("5 cheese", "5 queijos", "23.90-31.90", "Pizza sauce, mozzarella, gorgonzola, parmesan, provolone, catupiry, olives and oregano", None),
  ("Bacon", "", "23.90-31.90", "Pizza sauce, mozzarella, bacon, olives and oregano", None),
  ("Broccoli with bacon", "", "24.90-32.90", "Pizza sauce, mozzarella, broccoli, bacon, catupiry, cheddar, olives and oregano", None),
  ("Calabresa", "", "24.90-32.90", "Pizza sauce, mozzarella, smoked sausage, onions, olives and oregano", "calabresa"),
  ("Calabresa with bacon", "", "24.90-32.90", "Pizza sauce, mozzarella, smoked sausage, bacon, olives and oregano", None),
  ("Canadian bacon with catupiry", "Lombinho", "24.90-32.90", "Pizza sauce, mozzarella, Canadian bacon, pineapple, catupiry, olives and oregano", None),
  ("Carnivore", "", "23.90-31.90", "Pizza sauce, mozzarella, pepperoni, bacon, Italian sausage, green bell peppers and mushrooms", None),
  ("Carne seca BBQ", "", "24.90-32.90", "Tomato sauce, mozzarella, shredded beef, BBQ sauce and green onions", None),
  ("Chicken with bacon", "", "23.90-31.90", "Pizza sauce, chicken, mozzarella, bacon, olives and oregano", None),
  ("Chicken with catupiry", "Frango com catupiry", "25.90-33.90", "Pizza sauce, mozzarella, chicken, corn, catupiry, olives and oregano", None),
  ("Churrasco", "", "25.90-33.90", "Pizza sauce, mozzarella, provolone, steak, vinaigrette and catupiry", None),
  ("Hawaiian", "", "23.90-31.90", "Pizza sauce, mozzarella, ham, pineapple, olives and oregano", None),
  ("Hearts of palm", "Palmito", "24.90-32.90", "Pizza sauce, mozzarella, catupiry, hearts of palm, black olives and oregano", None),
  ("House style", "Moda da casa", "25.90-33.90", "Pizza sauce, mozzarella, calabresa, ham, Canadian bacon, tomatoes, eggs, bacon, corn, peas, onions, olives and oregano", None),
  ("Margherita", "", "23.90-31.90", "Pizza sauce, mozzarella, tomatoes, basil, olives and oregano", "margherita"),
  ("Mozzarella", "", "23.90-31.90", "Pizza sauce, mozzarella, tomatoes, olives and oregano", None),
  ("Nordestina", "", "25.90-33.90", "Pizza sauce, mozzarella, dried meat, catupiry, biquinho peppers, queijo coalho, olives, oregano and parsley", "nordestina"),
  ("Pepperoni", "", "23.90-31.90", "Pizza sauce, mozzarella, pepperoni, olives and oregano", None),
  ("Portuguese", "Portuguesa", "24.90-32.90", "Pizza sauce, ham, eggs, bacon, corn, peas, mozzarella, tomatoes, olives and oregano", None),
  ("Shrimp supreme", "", "25.90-33.90", "White sauce, mozzarella, catupiry, shrimp, parmesan, garlic sauce and parsley", None),
  ("Verde", "", "23.90-29.90", "Pizza sauce, mozzarella, oregano, arugula, sun-dried tomatoes and parmesan", None),
 ]),
 ("half", "Half and half", "Meio a meio", [
  ("Half and half savory", "Meia/meia salgada", "23.90-31.90", "Pick two savory flavors on one pizza", None),
  ("Half and half sweet", "Meia/meia doce", "23.90-31.90", "Pick two sweet flavors on one pizza", None),
 ]),
 ("sweet", "Sweet pizzas", "Pizza inteira doce", [
  ("Banana with cinnamon", "", "17.90-31.90", "Table cream, mozzarella, banana, sweetened condensed milk and cinnamon", None),
  ("Banana with Nutella", "", "17.90-31.90", "Table cream, mozzarella, banana and Nutella", "banana-nutella"),
  ("Brazilian peanut candy", "Paçoquita", "17.90-31.90", "Dulce de leche, paçoca and peanut brittle", None),
  ("Brigadeiro gourmet", "", "17.90-31.90", "Brigadeiro spread, chocolate sprinkles and traditional brigadeiro", None),
  ("Burnt coconut", "", "17.90-31.90", "Shredded coconut, dulce de leche and powdered sugar", None),
  ("Churros", "", "17.90-31.90", "Sweetened condensed milk, mozzarella, dulce de leche, cinnamon and powdered sugar", None),
  ("Coconut chocolate", "Prestígio", "17.90-31.90", "Nutella, sweetened condensed milk, shredded coconut and coconut chocolate", None),
  ("Ferrero", "", "17.90-31.90", "Nutella, chopped nuts, Ferrero Rocher and edible gold dust", None),
  ("Kinder", "", "17.90-31.90", "Nutella, Kinder Bueno and sweetened condensed milk", None),
  ("M&M's", "", "17.90-31.90", "Nutella and M&M's", None),
  ("Romeo and Juliet", "Romeu e Julieta", "17.90-31.90", "Table cream, mozzarella, catupiry and guava paste", None),
  ("Snowy banana", "Banana nevada", "17.90-31.90", "Table cream, mozzarella, banana, sweetened condensed milk, dulce de leche and Nido milk powder", None),
  ("Strawberry white chocolate", "", "17.90-31.90", "Table cream, mozzarella, white chocolate, strawberry and Kinder Bueno", None),
  ("Strawberry with Nutella", "", "17.90-31.90", "Nutella, strawberries and chocolate sprinkles", "strawberry-slice"),
  ("White chocolate", "", "17.90-31.90", "Table cream, mozzarella, white chocolate, green grapes and white chocolate wafer", None),
  ("Yoyo", "Chocolate branco e Nutella", "17.90-31.90", "Table cream, mozzarella, white chocolate and Nutella", None),
 ]),
 ("calzone", "Calzones", "", [
  ("Pepperoni calzone", "", "12.90", "Marinara, mozzarella, pepperoni, mushrooms and Italian sausage", None),
  ("Brasileiro", "", "15.90", "Marinara, mozzarella, dried meat, bell pepper, catupiry, onions and green olives", None),
  ("Frangão", "", "14.90", "Marinara, mozzarella, chicken, catupiry, cheddar, bacon and green olives", None),
  ("Do chefe", "", "15.90", "Marinara, mozzarella and the chef's secret blend with calabresa and green olives", None),
 ]),
 ("apps", "Appetizers", "", [
  ("Garlic bread", "", "7.90", "Mozzarella, parmesan, minced garlic and Italian seasoning", "garlic-bread"),
  ("Pepperoni bread", "", "9.90", "Mozzarella, pepperoni and Italian seasoning", None),
 ]),
 ("drinks", "Drinks", "", [
  ("Guaraná Antarctica (2 liter)", "", "7.50", "", None),
  ("Guaraná Antarctica (12 oz)", "", "3.50", "Regular or zero", None),
  ("Coca-Cola (2 liter)", "", "5.50", "", None),
  ("Mexican Coke", "", "4.50", "", None),
  ("Canned soda (12 oz)", "", "2.50", "Coca-Cola, Coke Zero, Sprite or Fresca", None),
  ("Perrier (11 oz)", "", "3.20", "", None),
  ("Dasani water (20 oz)", "", "2.50", "", None),
 ]),
]

# Signature pies for the photo carousel (all photos are the restaurant's own, from its Google listing)
SIGNATURE = [("Nordestina", "From Brazil's northeast"), ("Calabresa", "The Brazilian classic"),
             ("Margherita", "Simple and fresh"), ("Garlic bread", "Start here")]
SWEET = ["Strawberry with Nutella", "Banana with Nutella"]

# Menu tabs: tab id, label, the MENU groups shown in it
TABS = [("tab-savory", "Savory", ["savory"]), ("tab-sweet", "Sweet", ["sweet"]),
        ("tab-more", "Combos, calzones and sides", ["deal", "half", "calzone", "apps"]), ("tab-drinks", "Drinks", ["drinks"])]

GROUPS = {g[0]: g for g in MENU}
ITEMS = {i[0]: i for g in MENU for i in g[3]}
e = html.escape


def money(p):
    if "-" in p:
        return f'<small>from</small> ${p.split("-")[0]}'
    return f"${p}"


def full_money(p):
    if "-" in p:
        a, b = p.split("-")
        return f"${a} to ${b}, by size"
    return f"${p}"


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def tab_of(name):
    for tid, _, gids in TABS:
        for gid in gids:
            if any(i[0] == name for i in GROUPS[gid][3]):
                return tid
    return TABS[0][0]


def signature_html():
    out = []
    for name, tag in SIGNATURE:
        n, pt, price, desc, img = ITEMS[name]
        out.append(
            f'        <a class="sig" href="#item-{slug(n)}" data-tab="{tab_of(n)}">\n'
            f'          <img src="images/{img}.jpg" alt="{e(n)} from Brazil Pizza" width="640" height="512" loading="lazy">\n'
            f'          <span class="sig-tag">{e(tag)}</span>\n'
            f'          <span class="sig-body"><span class="sig-name">{e(n)}</span><span class="sig-desc">{e(desc)}</span>'
            f'<span class="sig-price">{money(price)}</span></span>\n'
            f'        </a>')
    return "\n".join(out)


def sweet_html():
    out = []
    for name in SWEET:
        n, pt, price, desc, img = ITEMS[name]
        out.append(
            f'          <a class="sweet-card" href="#item-{slug(n)}" data-tab="tab-sweet">'
            f'<img src="images/{img}.jpg" alt="{e(n)} sweet pizza from Brazil Pizza" width="640" height="512" loading="lazy">'
            f'<span class="sweet-cap"><b>{e(n)}</b><span>{money(price)}</span></span></a>')
    return "\n".join(out)


def item_html(it):
    n, pt, price, desc, img = it
    ph = f'<img class="it-img" src="images/{img}.jpg" alt="" width="640" height="512" loading="lazy">' if img else ''
    ptx = f'<span class="pt" lang="pt-BR">{e(pt)}</span>' if pt else ''
    d = f'<p class="desc">{e(desc)}</p>' if desc else ''
    return (f'<li class="item{" has-img" if img else ""}" id="item-{slug(n)}">{ph}<div class="it-body">'
            f'<h4>{e(n)}</h4>{ptx}{d}<span class="tag" title="{e(full_money(price))}">{money(price)}</span></div></li>')


def tabs_html():
    btns = []
    for k, (tid, label, _) in enumerate(TABS):
        sel = "true" if k == 0 else "false"
        ti = "" if k == 0 else ' tabindex="-1"'
        btns.append(f'        <button type="button" role="tab" id="{tid}-btn" aria-controls="{tid}" aria-selected="{sel}"{ti}>{e(label)}</button>')
    panels = []
    for tid, label, gids in TABS:
        parts = []
        for gid in gids:
            _, title, note, items = GROUPS[gid]
            nt = f' <span class="pt" lang="pt-BR">{e(note)}</span>' if note else ''
            cls = '' if len(gids) > 1 else ' class="sr"'
            lis = "\n".join("            " + item_html(it) for it in items)
            parts.append(f'          <h3 id="{gid}"{cls}>{e(title)}{nt}</h3>\n          <ul class="items">\n{lis}\n          </ul>')
        panels.append(f'        <div class="panel" role="tabpanel" id="{tid}" aria-labelledby="{tid}-btn" tabindex="0">\n'
                      + "\n".join(parts) + '\n        </div>')
    return "\n".join(btns), "\n".join(panels)


btns, panels = tabs_html()

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TEMPLATE = open('tools/template.html', encoding='utf-8').read()
page = (TEMPLATE.replace('{{SIGNATURE}}', signature_html()).replace('{{SWEET}}', sweet_html())
        .replace('{{TABS}}', btns).replace('{{PANELS}}', panels)
        .replace('{{ORDER}}', ORDER).replace('{{MAPS}}', MAPS).replace('{{EMBED}}', EMBED).replace('{{TEL}}', TEL)
        .replace('{{INSTA}}', INSTA))
assert '{{' not in page
open('index.html', 'w', encoding='utf-8').write(page)
print('built', len(page), 'bytes;', sum(len(g[3]) for g in MENU), 'menu items')
