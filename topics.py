# 30 günlük konu listesi. Kodlanmış günler: 1-9 (kalanlar sırayla eklenecek)
R=(255,255,255)
def stack(**k): return dict(type="stack", **k)

TOPICS = {
1: dict(kind="food", title="Dev pizza nasıl yapılır?", next="Bisiklet tamiri", fx="confetti",
  caps=["Dev pizza nasıl yapılır?","1. Hamuru aç","2. Sosu sür","3. Bol peynir!","4. Malzemeleri ekle","Fırına!","Pizzaya bak, güldü!","Afiyet olsun!"],
  spec=dict(type="round", style="ellipse", base=(247,226,178), baked=(224,150,72), ops=[
    dict(op="spread", color=(214,64,48)),
    dict(op="scatter", kind="sprinkle", n=140, colors=[(255,238,170),(255,224,130)], sc=1.3, color=(250,222,130), baked=(244,188,78)),
    dict(op="scatter", kind="pep", n=7, colors=[(196,48,44)], gap=.16),
  ])),
2: dict(kind="repair", title="Patlayan bisiklet lastiği nasıl tamir edilir?", next="Dev pasta", fx="bubbles",
  caps=["Lastik patlamış!","1. Neresi bozuk bakalım","2. Çiviyi çıkar","3. Lastiği şişir","4. Parlat","Deneme sürüşü!","Bisiklet çok mutlu!","Tamir bitti!"],
  spec=dict(obj="bike", tools=["wrench","wrench","pump"])),
3: dict(kind="food", title="Gökkuşağı pasta nasıl yapılır?", next="Bozuk robot tamiri", fx="confetti",
  caps=["Gökkuşağı pasta yapalım!","1. Kırmızı ve turuncu kat","2. Sarı ve yeşil kat","3. Mavi ve mor kat","4. Krema ve şekerler","Süsleme zamanı!","Pasta gülümsedi!","Afiyet olsun!"],
  spec=stack(face=3, fs=1.5, layers=[
    dict(shape="slab",color=(235,70,70),w=240,h=50,step=0), dict(shape="slab",color=(255,250,245),w=242,h=12,step=0),
    dict(shape="slab",color=(255,150,60),w=240,h=50,step=0), dict(shape="slab",color=(255,250,245),w=242,h=12,step=1),
    dict(shape="slab",color=(255,215,70),w=238,h=50,step=1), dict(shape="slab",color=(255,250,245),w=240,h=12,step=1),
    dict(shape="slab",color=(110,200,110),w=236,h=50,step=1), dict(shape="slab",color=(255,250,245),w=238,h=12,step=2),
    dict(shape="slab",color=(90,170,240),w=234,h=50,step=2), dict(shape="slab",color=(255,250,245),w=236,h=12,step=2),
    dict(shape="slab",color=(160,110,220),w=232,h=50,step=2),
    dict(shape="swirl",color=(255,190,215),w=200,h=110,step=3), dict(shape="heart",color=(255,80,120),w=60,h=50,step=3)])),
4: dict(kind="repair", title="Bozuk robotu birlikte onaralım", next="Dev hamburger", fx="stars",
  caps=["Robot bozuldu!","1. Neresi bozuk bakalım","2. Kolu yerine tak","3. Teli bağla","4. Parlat","Robot çalışıyor mu?","Robot dans ediyor!","Tamir bitti!"],
  spec=dict(obj="robot", tools=["screwdriver","wrench","screwdriver"])),
5: dict(kind="food", title="Dev hamburger kulesi", next="Altınla kırık fincan tamiri", fx="confetti",
  caps=["Dev hamburger yapalım!","1. Alt ekmeği koy","2. Köfte ve peynir","3. Marul ve domates","4. Üst ekmeği kapat","Son dokunuş!","Hamburger güldü!","Afiyet olsun!"],
  spec=stack(face=1, fs=1.3, layers=[
    dict(shape="slab",color=(235,185,110),w=215,h=50,step=0),
    dict(shape="slab",color=(120,70,45),w=228,h=48,step=1), dict(shape="slab",color=(255,205,50),w=236,h=16,step=1),
    dict(shape="wavy",color=(90,190,80),w=244,h=26,step=2), dict(shape="slab",color=(230,60,50),w=214,h=26,step=2),
    dict(shape="dome",color=(235,185,110),w=222,h=140,step=3,seeds=[(-80,-10),(-30,-45),(40,-30),(90,0),(10,10),(-120,10)])])),
6: dict(kind="repair", title="Kırık fincan altınla birleşiyor", next="Dondurma kulesi", fx="stars",
  caps=["Fincan kırılmış!","1. Parçalara bakalım","2. Parçaları birleştir","3. Altın yapıştırıcı","4. Parlat","Fincan hazır!","Fincan gülümsedi!","Tamir bitti!"],
  spec=dict(obj="cup", tools=["glue","glue","glue"])),
7: dict(kind="food", title="Dondurma kulesi yapalım", next="Ayıcığın dikişi", fx="hearts",
  caps=["Dondurma kulesi yapalım!","1. Bardağı hazırla","2. İlk iki top","3. Üçüncü top ve sos","4. Kiraz ve şekerler","Son dokunuş!","Dondurma güldü!","Afiyet olsun!"],
  spec=stack(face=2, fs=1.0, layers=[
    dict(shape="cup",color=(190,225,245),w=150,h=150,step=0),
    dict(shape="ball",color=(255,170,200),w=0,h=160,step=1), dict(shape="ball",color=(150,225,190),w=0,h=140,step=1),
    dict(shape="ball",color=(150,100,70),w=0,h=125,step=2,drip=(110,60,40)),
    dict(shape="ball",color=(230,40,60),w=0,h=48,step=3), dict(shape="sprinkles",color=R,w=140,h=0,step=3,cols=[(255,90,90),(90,170,255),(255,210,60),(110,210,120)])])),
8: dict(kind="repair", title="Ayıcığın dikişi nasıl atılır?", next="Krep kulesi", fx="hearts",
  caps=["Ayıcık yırtılmış!","1. Neresi yırtık bakalım","2. Pamuğu içeri koy","3. Dikişi at","4. Fırçala","Ayıcık hazır mı?","Ayıcık göz kırptı!","Tamir bitti!"],
  spec=dict(obj="teddy", tools=["needle","needle","needle"])),
9: dict(kind="food", title="Krep kulesi nasıl yapılır?", next="Katmanlı sürpriz", fx="hearts",
  caps=["Krep kulesi yapalım!","1. İlk krepler","2. Krepleri üst üste koy","3. Kule büyüyor","4. Tereyağı, şurup, çilek","Son dokunuş!","Kule güldü!","Afiyet olsun!"],
  spec=stack(face=3, fs=1.3, layers=[
    dict(shape="slab",color=(238,190,120),w=232,h=36,step=0), dict(shape="slab",color=(228,176,104),w=230,h=36,step=0),
    dict(shape="slab",color=(238,190,120),w=232,h=36,step=1), dict(shape="slab",color=(228,176,104),w=230,h=36,step=1),
    dict(shape="slab",color=(238,190,120),w=232,h=36,step=2), dict(shape="slab",color=(228,176,104),w=230,h=36,step=2),
    dict(shape="slab",color=(238,190,120),w=232,h=36,step=2),
    dict(shape="slab",color=(255,235,130),w=70,h=18,step=3), dict(shape="syrup",color=(150,80,40),w=200,h=6,step=3),
    dict(shape="ball",color=(230,45,70),w=0,h=64,step=3)])),
}
for d,t in TOPICS.items(): t["day"]=d
