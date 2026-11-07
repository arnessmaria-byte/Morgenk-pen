# nr, navn, S (sentralitet målt mot Skriften og den tidligste kirken), D (splittelseskraft), A (aktualitet), U (utbredelse)
items = [
(1,"Rettferdiggjørelsen",9,10,6,9),(2,"Autoritet: Skrift og tradisjon",9,10,7,10),(3,"Treenigheten og Kristi guddom",10,9,4,10),
(4,"Samkjønnet samliv og ekteskap",6,9,10,10),(5,"Paven",5,10,5,10),(6,"Nattverden",8,9,5,10),(7,"Bibelsyn",7,7,8,9),
(8,"Dåpen",8,8,5,10),(9,"Predestinasjon og fri vilje",7,8,6,8),(10,"Kristi to naturer",8,9,2,7),(11,"Filioque",5,9,3,8),
(12,"Kvinners ordinasjon",5,8,9,10),(13,"Helvete og de siste ting",7,4,7,9),(14,"Forsoningen",8,4,6,9),
(15,"Frelse utenfor Kristus",8,4,7,10),(16,"Kirkens vesen og apostolisk suksesjon",6,9,5,10),(17,"Abort",5,4,9,10),
(18,"Skapelse og evolusjon",5,4,7,9),(19,"Arvesynden",6,6,3,9),(20,"Mariologi",5,7,4,9),(21,"Skjærsild, bønn for de døde og avlat",4,9,3,8),
(22,"Helgenpåkallelse og relikvier",3,7,3,8),(23,"Sakramentene",5,7,2,9),(24,"Jesu legemlige oppstandelse",10,3,5,9),
(25,"Bibelens kanon",6,6,3,9),(26,"Nådegavene",6,6,7,8),(27,"Israel og kirken",5,3,8,6),(28,"Tusenårsriket og bortrykkelsen",4,4,6,6),
(29,"Kirkeordning",5,7,3,9),(30,"Kirke og stat",4,6,6,9),(31,"Frelsesvisshet og frafall",6,5,4,7),(32,"Liberal teologi",7,6,7,8),
(33,"Skilsmisse og gjengifte",6,4,6,9),(34,"Bilder og ikoner",3,7,2,8),(35,"Jomfrufødselen",8,3,4,9),
(36,"Komplementarisme eller egalitarisme",5,5,8,8),(37,"Krig og pasifisme",5,4,6,8),(38,"Kjønnsidentitet",4,4,9,8),
(39,"Prestesølibatet",3,5,5,7),(40,"Prevensjon",3,3,5,8),(41,"Lov og evangelium",7,5,3,7),(42,"Liturgi og gudstjeneste",4,5,5,8),
(43,"Tvang i trossaker",5,5,4,8),(44,"Velstandsteologi",5,3,7,6),(45,"Den historiske Adam",6,2,6,6),(46,"Slaveriet",4,6,2,5),
(47,"Eutanasi",4,2,8,8),(48,"Mormoner, Jehovas vitner og lignende",6,5,4,4),(49,"Sabbat eller søndag",4,3,3,3),
(50,"Økumenikk",5,5,5,9),(51,"Sex før ekteskapet og samboerskap",5,2,6,9),(52,"Frigjøringsteologi og sosialt evangelium",3,3,3,5),
(53,"Rasisme og etnisk kirke",6,5,6,8),(54,"Misjon og proselytisme",6,3,4,7),(55,"Gnostisisme og Markion",8,7,2,4),
(56,"Donatismen og gjendåp",4,6,2,5),(57,"Påskedatoen",3,6,4,8),(58,"Kirketukt",5,3,4,7),(59,"Tro og vitenskap",3,3,6,8),
(60,"Investiturstriden",1,5,1,3),(61,"Korstog og hellig krig",4,4,3,6),(62,"Modalisme",7,5,3,3),(63,"Pietisme og lekpredikanter",3,4,2,3),
(64,"Synodalitet og lekfolkets makt",3,3,5,6),(65,"Kristen nasjonalisme",4,3,8,6),(66,"Dødsstraff",3,2,4,6),
(67,"Rikdom, fattigdom og renter",6,2,4,8),(68,"Hesykasme og Guds energier",2,4,2,4),(69,"Guds lidelse og åpen teisme",4,2,4,5),
(70,"Sjelens udødelighet",5,3,3,6),(71,"Hermeneutikk",4,4,4,7),(72,"Gudsspråk og feministteologi",5,3,5,6),
(73,"Nattverdfellesskap mellom kirker",5,5,5,8),(74,"Klosterlivet",3,5,2,6),(75,"Monotelittismen",4,6,1,5),
(76,"Naturlig teologi",3,2,2,4),(77,"Vekkelsesmetoder",2,3,3,4),(78,"Helliggjørelse og fullkommenhet",5,4,2,5),
(79,"Grunntekst og bibeloversettelser",3,3,4,5),(80,"Musikk i gudstjenesten",2,3,4,6),(81,"Åndelig krigføring og eksorsisme",4,2,4,5),
(82,"Jurisdiksjonsstriden i ortodoksien (Ukraina)",2,6,7,5),(83,"Skaperverket og klima",3,2,6,8),(84,"Montanisme og ny åpenbaring",5,5,1,3),
(85,"Adiafora og kirkelige skikker",3,4,2,5),(86,"Sønnens underordning (ESS)",4,2,3,3),(87,"Kunstig befruktning og bioteknologi",2,1,5,7),
(88,"Alkohol og avholdssak",2,3,2,5),(89,"Kenosis",4,2,2,3),(90,"Datering av gjenkomsten",3,3,3,3),(91,"Kirkeasyl og migrasjon",3,1,6,6),
(92,"Barnekommunion",4,3,3,7),(93,"Faste",5,2,2,7),(94,"Høytider og jul",2,2,3,6),(95,"Alternativ spiritualitet",3,1,5,6),
(96,"Tiende",3,1,3,6),(97,"Kremasjon",3,1,3,7),(98,"Satan og demoner",7,2,3,8),(99,"Hodeplagg for kvinner",4,2,3,7),
(100,"Kristi nedfart til dødsriket",5,2,2,8),(101,"Usyret eller syret brød i nattverden",3,6,1,8),(102,"Kalenderskismaet",2,5,3,5),
]
W=(0.45,0.20,0.20,0.15)
rows=[]
for n,name,s,d,a,u in items:
    tot=s*W[0]+d*W[1]+a*W[2]+u*W[3]
    rows.append((round(tot,2),s,n,name,s,d,a,u))
rows.sort(key=lambda r:(-r[0],-r[1],r[2]))
assert len({r[2] for r in rows})==102
for i,r in enumerate(rows): print(i+1, r[2], r[3], r[4:8], r[0])
