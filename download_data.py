# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:09:51 2021

@author: scikit-learn/doc/tutorial/text_analytics/data/languages/fetch_data.py/ changed for my purposes. Thanks :)
 
"""

import os
from urllib.request import Request, build_opener

import lxml.html
from lxml.etree import ElementTree
import numpy as np

import codecs


pages = {
    'sr' : ["https://startit.rs/uri-svi-frilenseri-ce-biti-tretirani-jednako-odluka-mozda-ne-bude-u-petak/", 
            "https://startit.rs/brojevi-telefona-facebook-korisnika-prodaju-se-preko-telegram-bota-za-20-dolara/", 
            "https://www.helloworld.rs/blog/Sta-je-code-review-i-zasto-je-znacajan/11114",
            "https://mondo.rs/Sport/Fudbal/a1406429/deportivo-la-korunja-osvojena-titula-u-spaniji.html",
            "https://mondo.rs/Sport/Kosarka/a1405559/nba-price-kosarka-nba-liga-keron-batler-hapsenje-dilovanje-droge.html",
            "https://mondo.rs/Sport/Fudbal/a1427493/mauro-kamoranezi-crvena-zvezda-milan-dejan-stankovic.html",
            "https://mondo.rs/Sport/Fudbal/a1424010/dragan-stojkovic-piksi-crvena-zvezda-goran-milojevic-prvi-znao-da-dolazi-mondo-intervju.html"],
    
    'sl' : ["https://ekipa.svet24.si/clanek/pogled/andrej-miljkovic/5fec4f9b4510e/primoz-dovolj-je-tadeju-dolgujes-opravicilo", 
            "https://ekipa.svet24.si/clanek/pogled/miha-andolsek/5fc281e96d2ac/diego-bozja-roka-ki-se-je-rokovala-s-hudicem",
            "https://ekipa.svet24.si/clanek/pogled/primoz-salmic/5f830473680bd/skregano-z-zdravo-pametjo-pardon-skrekano"],
    
    'hr' : ["https://www.dalmacijadanas.hr/zdravstveni-savjeti-dr-zeljke-roje-kako-pobijediti-alergijski-rinitis/",
            "https://www.dalmacijadanas.hr/ivo-tartaglia-ili-kako-je-split-zaboravio-svog-velikana/",
            "https://www.dalmacijadanas.hr/kolumna-nikole-barbarica-10-pravila-kako-bi-se-roditelji-trebali-ponasati-na-prvom-treningu-svog-djeteta/",
            "https://www.dalmacijadanas.hr/splicanin-mora-proci-1-600-km-u-24-sata-od-splita-do-verone-i-nazad-zeljan-rakela-sjeda-na-hondu-x-adv-750cc-rezervoara-svega-13-litara/"],
    
    'mk' : ["https://www.novamakedonija.com.mk/prilozi/globus/%d0%b1%d0%b0%d1%98%d0%b4%d0%b5%d0%bd-%d0%b3%d0%b8-%d0%b2%d1%80%d0%b0%d1%9c%d0%b0-%d1%81%d0%b0%d0%b4-%d0%b2%d0%be-%d0%bf%d0%b0%d1%80%d0%b8%d1%81%d0%ba%d0%b8%d0%be%d1%82-%d0%ba%d0%bb%d0%b8%d0%bc%d0%b0/",
            "https://www.novamakedonija.com.mk/makedonija/politika/%d0%bc%d0%b0%d0%ba%d0%b5%d0%b4%d0%be%d0%bd%d0%b8%d1%98%d0%b0-%d0%ba%d0%b0%d0%ba%d0%be-%d1%87%d0%bb%d0%b5%d0%bd%d0%ba%d0%b0-%d0%bd%d0%b0-%d0%bd%d0%b0%d1%82%d0%be-%d0%b7%d0%bd%d0%b0%d1%87%d0%b0%d1%98/",
            "https://www.novamakedonija.com.mk/prilozi/globus/%d1%80%d1%83%d1%81%d0%b8%d1%98%d0%b0-%d1%81%d0%b5-%d0%bf%d0%be%d0%b4%d0%b3%d0%be%d1%82%d0%b2%d1%83%d0%b2%d0%b0-%d0%b7%d0%b0-%d0%b2%d0%be%d0%b5%d0%bd%d0%b0-%d0%b4%d0%be%d0%bc%d0%b8%d0%bd%d0%b0%d1%86/",
            "https://vecer.mk/komentari-i-analizi/vakcinaciski-nacionalizam-javni-tajni-i-naivnost-na-brisel/",
            "https://vecer.mk/balkan/801205/"],
    
    'bih': ["https://avaz.ba/vijesti/kolumne/626492/bezobrazna-bh-vlast",
            "https://avaz.ba/globus/svijet/627986/biontech-obecao-isporuku-75-miliona-dodatnih-doza-vakcina-eu",
            "https://sport.avaz.ba/borilacki-sportovi/628008/overem-zeli-otici-u-penziju-sa-titulom-prvaka",
            "https://sport.avaz.ba/kosarka/627919/bubakar-se-izvinio-halilovicu-nisam-pokazao-dobar-primjer-mladim",
            "https://sport.avaz.ba/nogomet/628003/barcelone-se-vise-ne-sjeca-nejmar-sada-sretan-u-psg-u",
            "https://sport.avaz.ba/kosarka/627641/lilard-pogodio-dvije-trojke-za-devet-sekundi-i-donio-portlandu-pobjedu",
            "https://www.oslobodjenje.ba/vijesti/bih/stanivukovic-novo-remek-djelo-cucuna-xiv-zicana-ograda-od-nevjerovatnih-120-000-km-626323",
            "https://www.oslobodjenje.ba/vijesti/bih/cenic-dodik-je-prekrizen-u-medunarodnoj-zajednici-i-kod-vucica-626283",
            "https://www.oslobodjenje.ba/vijesti/region/hrvatsku-knjizevnicu-napali-sto-se-vakcinisala-u-srbiji-mislila-sam-da-sam-pozvana-kao-umjetnica-a-ne-kao-kradljivica-626322"],
    
    'hu': ["https://24.hu/tudomany/2021/02/01/gyerek-trianon-haboru-gyermekmentes-humanitarius-akcio/", 
           "https://24.hu/kozelet/2021/02/01/vagyonnyilatkozat-varga-judit-pinter-sandor-szabo-tunde-palkovics-laszlo/",
           "https://24.hu/tudomany/2021/02/01/idojaras-front-meleg-hideg/",
           "https://24.hu/kultura/2021/02/01/citadella-felujitas-meszaros-lorinc-garancsi-istvan-market-zaev/"],
    
    'bg': ["https://www.24chasa.bg/novini/article/9472405",
           "https://www.24chasa.bg/region/article/9472241",
           "https://www.24chasa.bg/novini/article/9472085",
           "https://www.24chasa.bg/mnenia/article/9471752",
           "https://www.24chasa.bg/novini/article/9471342"],
    
    'alb': ["http://www.panorama.com.al/sport/makth-per-12-minuta-ne-apolonia-tirana-delegati-cela-kishte-krisje-te/",
            "http://www.panorama.com.al/sport/e-bujshme-shqiperia-mund-te-fitoje-ndeshjen-me-angline-ne-tavoline-ja-arsyeja/",
            "http://www.panorama.com.al/sport/shtyrja-eshte-e-demshme-per-klubet-cela-lushnja-me-bind-por-i-duhen-terrene/"]
}


html_folder = 'html'
text_folder = 'paragraphs'
short_text_folder = 'short_paragraphs'
n_words_per_short_text = 5

if not os.path.exists(html_folder):
    os.makedirs(html_folder)
    
for lang, pages in pages.items():
    
    text_lang_folder = os.path.join(text_folder, lang)
    
    if not os.path.exists(text_lang_folder):
        os.makedirs(text_lang_folder)
        
    short_text_lang_folder = os.path.join(short_text_folder, lang)
    if not os.path.exists(short_text_lang_folder):
        os.makedirs(short_text_lang_folder)
    
    opener = build_opener()
    
    for page in pages:
        html_filename = os.path.join(html_folder, lang + '.html')
        
        print("Downloading %s" %page)
            
        request = Request(page)
        request.add_header('User-Agent', 'OpenAnything/1.0')
        html_content = opener.open(request).read()
        open(html_filename, 'wb').write(html_content)
        
        with codecs.open(html_filename, 'r', 'utf-8') as html_file:
            html_content = html_file.read()
            
            
        tree = ElementTree(lxml.html.document_fromstring(html_content))
        i = 0
        j = 0
        
        for p in tree.findall('//p'):
            content = p.text_content()
            
            if len(content) < 100:
                continue
            
            text_filename = os.path.join(text_lang_folder,'%s_%04d.txt' % (lang, i))
            print("Writing %s" % text_filename)
            open(text_filename, 'wb').write(content.encode('utf-8', 'ignore'))
            i += 1

            if lang in ('zh', 'ja'):
                continue
            
            words = content.split()
            n_groups = len(words) / n_words_per_short_text
            
            if n_groups < 1:
                continue
            
            groups = np.array_split(words, n_groups)

            for group in groups:
                small_content = " ".join(group)

                short_text_filename = os.path.join(short_text_lang_folder, '%s_%04d.txt' % (lang, j))
                print("Writing %s" % short_text_filename)
                open(short_text_filename, 'wb').write(small_content.encode('utf-8', 'ignore'))
                
                j += 1
                
                if j >= 1000:
                    break
        