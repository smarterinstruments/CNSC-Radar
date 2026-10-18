"""Seed of the CNSC member master list.

Source: cnsc-katalog.html (CNSC service catalogue, Aug 2026, 52 members) reconciled with
https://www.semicz.cz/memberlist/ on 18 Oct 2026 (adds Advacam). Writes data/members.json.
Fields: id, n (name), short, city, url, s (value-chain segment), acadChip, partnerIn, cs, en, logo,
li (LinkedIn company slug, filled in by tools/linkedin_lookup), note.
"""
import json, os, re, unicodedata

LG = "https://www.semicz.cz/wp-content/uploads/"
M = [
 # 01 design
 ("Codasip","Codasip","Brno · Praha","https://codasip.com","design",False,[],"Procesorová IP na bázi RISC-V a nástroje pro automatizaci návrhu procesorů.","RISC-V processor IP and processor design automation tools.","2024/12/codasip-1.png"),
 ("ASICentrum (EM Microelectronic)","ASICentrum","Praha","https://www.asicentrum.cz","design",False,[],"Návrh ultra-nízkopříkonových ASIC a SoC pro hodinky, IoT a senzoriku.","Ultra-low-power ASIC and SoC design for watches, IoT and sensing.","2024/12/asicentrum-1.png"),
 ("Analog Bits","Analog Bits","Praha","https://www.analogbits.com","design",False,[],"Analogová a mixed-signal IP: PLL, SerDes, senzory a I/O pro pokročilé uzly.","Analog and mixed-signal IP: PLLs, SerDes, sensors and I/O for advanced nodes.","2024/12/analogbits-1.png"),
 ("Allegro MicroSystems","Allegro","Praha","https://www.allegromicro.com","design",False,[],"Návrh senzorových a výkonových integrovaných obvodů pro automotive a průmysl.","Sensor and power IC design for automotive and industrial markets.","2024/12/allegro-1.png"),
 ("Tropic Square","Tropic Square","Praha","https://tropicsquare.com","design",False,[],"Otevřené a auditovatelné bezpečnostní čipy (secure elements).","Open and auditable secure element chips.","2025/11/tropicsq-kopie.webp"),
 ("DynaNIC Semiconductor","DynaNIC","Brno","https://www.semicz.cz/memberlist/dynanic-company-profile/","design",False,[],"Návrh čipů pro síťové aplikace a akceleraci datových center.","Chip design for networking and data-center acceleration.","2025/06/dynanic-1.webp"),
 ("Renesas Electronics","Renesas","Praha","https://www.renesas.com","design",False,[],"Vývojové centrum mikrokontrolérů a embedded řešení.","Development centre for microcontrollers and embedded solutions.","2025/01/renesas.webp"),
 ("STMicroelectronics","ST","Praha","https://www.st.com","design",False,[],"Návrhové centrum integrovaných obvodů globálního výrobce polovodičů.","IC design centre of a global semiconductor manufacturer.","2025/01/st.webp"),
 ("NXP Semiconductors","NXP","Rožnov p. R.","https://www.nxp.com","design",False,[],"Vývoj a testování čipů pro automotive, IoT a zabezpečenou konektivitu.","Development and test of chips for automotive, IoT and secure connectivity.","2025/01/nxp.webp"),
 ("edhouse","edhouse","Zlín","https://www.edhouse.cz","design",False,[],"Vývoj software a hardware pro polovodičový průmysl a embedded systémy.","Software and hardware development for the semiconductor industry and embedded systems.","2026/02/edhouse.png"),
 # 02 materials
 ("Crytur","Crytur","Turnov","https://www.crytur.com","materials",False,[],"Syntetické krystaly, scintilátory a optické komponenty světové úrovně.","World-class synthetic crystals, scintillators and optical components.","2025/04/crytur.webp"),
 ("UJP Praha","UJP Praha","Praha","https://www.ujp.cz","materials",False,[],"Výzkum a výroba speciálních kovových materiálů a povlaků.","Research and production of special metallic materials and coatings.","2025/01/ujp.webp"),
 # 03 fab
 ("onsemi","onsemi","Rožnov p. R.","https://www.onsemi.com","fab",False,[],"Výroba křemíkových desek a čipů; centrum výkonových polovodičů (SiC).","Wafer and chip manufacturing; power semiconductor (SiC) hub.","2025/01/onsemi.webp"),
 ("Argotech","Argotech","Trutnov","https://www.argotech.cz","fab",False,[],"Pokročilé pouzdření, mikroelektronická montáž a optoelektronika.","Advanced packaging, microelectronic assembly and optoelectronics.","2024/12/argotech-1.png"),
 # 04 equipment
 ("SVCS Process Innovation","SVCS","Brno · Valašské Meziříčí","https://www.svcs.cz","equipment",False,[],"Difuzní a LPCVD pece a procesní zařízení pro výrobu polovodičů.","Diffusion and LPCVD furnaces and process equipment for semiconductor manufacturing.","2024/12/svcs-1.png"),
 ("Edwards","Edwards","Lutín","https://www.edwardsvacuum.com","equipment",False,[],"Vakuová technika a systémy pro čisté výrobní procesy.","Vacuum technology and abatement systems for clean manufacturing.","2025/09/edwards.webp"),
 ("Swagelok Central Fluidsystems","Swagelok","Praha","https://www.swagelok.com","equipment",False,[],"Fluidní systémy a komponenty pro rozvody procesních plynů.","Fluid system components for process gas distribution.","2026/05/swagelok.webp"),
 ("EP Rožnov","EP Rožnov","Rožnov p. R.","https://www.semicz.cz/memberlist/eproznov-company-profile/","equipment",False,[],"Inženýring čistých prostor a technologických celků pro elektroniku.","Cleanroom and technology engineering for the electronics industry.","2026/02/EProznov.jpg"),
 ("Activair","Activair","Opava","https://www.semicz.cz/memberlist/activair-company-profile/","equipment",False,[],"Čisté prostory, vzduchotechnika a klimatizace pro náročné provozy.","Cleanrooms, HVAC and air-handling for demanding facilities.","2026/02/activair_logo.webp"),
 ("Stroza","Stroza","Rožnov p. R.","https://www.stroza.cz","equipment",False,[],"Strojírenská výroba a servis pro polovodičové provozy.","Mechanical engineering and services for semiconductor plants.","2025/01/stroza.webp"),
 ("Streicher","Streicher","Plzeň","https://www.streicher.cz","equipment",False,[],"Strojírenství a výroba technologických zařízení.","Machinery and technological equipment manufacturing.","2025/01/streicher.webp"),
 ("Leadec","Leadec","Praha","https://www.leadec-services.com","equipment",False,[],"Technické služby a údržba průmyslových a výrobních areálů.","Technical facility services and maintenance for industrial sites.","2025/04/leadec.webp"),
 # 05 test
 ("Tescan","Tescan","Brno","https://www.tescan.com","test",False,[],"Elektronové mikroskopy a FIB-SEM systémy pro analýzu vad a circuit edit.","Electron microscopes and FIB-SEM systems for failure analysis and circuit edit.","2025/01/tescan.webp"),
 ("Thermo Fisher Scientific","Thermo Fisher","Brno","https://www.thermofisher.com","test",False,[],"Vývoj a výroba elektronových mikroskopů pro polovodičový průmysl.","Development and manufacturing of electron microscopes for the semiconductor industry.","2025/01/thermofisher.webp"),
 ("Unites Systems","Unites","Valašské Meziříčí","https://www.unites.cz","test",False,[],"Testery a manipulátory pro finální testování integrovaných obvodů.","Testers and handlers for final IC testing.","2025/01/unites.webp"),
 ("HTest","HTest","Praha","https://www.htest.cz","test",False,[],"Měřicí a testovací technika pro elektroniku a vývojové laboratoře.","Measurement and test instrumentation for electronics and R&D labs.","2025/04/htest.webp"),
 ("Advacam","Advacam","Praha","https://www.advacam.com","test",False,[],"Pixelové detektory záření a kamery pro částicové zobrazování (Timepix) pro NDT, elektronovou mikroskopii, materiálovou analýzu a vesmírnou dozimetrii.","Radiation imaging pixel detectors and particle-tracking cameras (Timepix) for NDT, electron microscopy, material analysis and space dosimetry.",None),
 # 06 apps
 ("Hitachi Energy","Hitachi Energy","Praha","https://www.hitachienergy.com","apps",False,[],"Výkonové polovodiče a řešení pro energetické sítě.","Power semiconductors and solutions for energy grids.","2025/01/hitachie.webp"),
 ("ESC Aerospace","ESC Aerospace","Praha","https://www.esc-aerospace.com","apps",False,[],"Spolehlivá elektronika a software pro vesmírné a bezpečnostní aplikace.","High-reliability electronics and software for space and security applications.","2025/01/esc-aero.webp"),
 ("MycroftMind","MycroftMind","Brno","https://www.mycroftmind.com","apps",False,[],"Edge AI a analytika pro energetiku a průmyslový IoT.","Edge AI and analytics for energy and industrial IoT.","2025/09/microftmind-kopie.webp"),
 ("Inference Technologies","Inference Technologies","Praha","https://www.semicz.cz/memberlist/inference-technologies-company-profile/","apps",False,[],"AI řešení pro optimalizaci výrobních a inspekčních procesů.","AI solutions for manufacturing and inspection process optimisation.","2025/01/interfer.webp"),
 ("TechSoft Engineering","TechSoft","Praha","https://www.techsoft-eng.cz","apps",False,[],"Inženýrské simulace (CAE/ANSYS) pro návrh čipů, pouzder a chlazení.","Engineering simulation (CAE/ANSYS) for chip, package and thermal design.","2025/01/techsoft.webp"),
 ("Smarter Instruments","Smarter Instruments","Brno","https://www.semicz.cz/memberlist/smarter-instruments/","apps",False,[],"Chytrá měřicí a přístrojová technika.","Smart measurement and instrumentation technology.","2025/01/smarter-in.webp"),
 # 07 research
 ("VUT v Brně (BUT)","VUT Brno","Brno","https://www.vut.cz","research",True,["design","materials"],"Mikroelektronika a projekt Chips of Europe; nové studijní programy. Návrh čipů: návrh integrovaných obvodů, ekosystém RISC-V a akademické centrum návrhu čipů ACDRC.","Microelectronics and the Chips of Europe project; new study programmes. Chip design: IC design, the RISC-V ecosystem and the ACDRC academic chip design research centre.","2024/12/vut-1.png"),
 ("Masarykova univerzita","MUNI","Brno","https://www.muni.cz","research",True,["design","materials"],"Informatika, kyberbezpečnost a vzdělávání pro polovodičový průmysl. Návrh čipů: funkční a formální verifikace návrhu, číslicové zpracování signálů a rychlých dat.","Computer science, cybersecurity and education for the semiconductor industry. Chip design: functional and formal design verification, digital signal and fast data processing.","2025/01/muni.webp"),
 ("ČVUT v Praze","ČVUT","Praha","https://www.cvut.cz","research",True,["design"],"Elektrotechnika a mikroelektronika. Návrh čipů: návrh analogových i číslicových integrovaných obvodů a výchova návrhářů čipů.","Electrical engineering and microelectronics. Chip design: analog and digital IC design and education of chip designers.","2025/01/ctu.webp"),
 ("Univerzita Karlova","UK","Praha","https://www.cuni.cz","research",False,["test"],"Fyzika polovodičů a materiálový výzkum.","Semiconductor physics and materials research.","2025/01/charles-uni.webp"),
 ("VŠCHT Praha","VŠCHT","Praha","https://www.vscht.cz","research",False,[],"Chemické technologie a materiály pro mikro- a nanoelektroniku.","Chemical technologies and materials for micro- and nanoelectronics.","2026/02/VSCHT.png"),
 ("Západočeská univerzita v Plzni","ZČU","Plzeň","https://www.zcu.cz","research",False,[],"Elektrotechnika, materiálový výzkum a inteligentní systémy.","Electrical engineering, materials research and smart systems.","2025/01/zcu.webp"),
 ("VŠB-TU Ostrava","VŠB-TUO","Ostrava","https://www.vsb.cz","research",False,[],"Nanotechnologie, IT a materiálové inženýrství.","Nanotechnology, IT and materials engineering.","2025/04/vsb.webp"),
 ("Technická univerzita v Liberci","TUL","Liberec","https://www.tul.cz","research",False,[],"Materiálový výzkum, nanotechnologie a mechatronika.","Materials research, nanotechnology and mechatronics.","2025/04/tul.webp"),
 ("Univerzita Pardubice","UPCE","Pardubice","https://www.upce.cz","research",False,[],"Chemie materiálů a elektrotechnika.","Materials chemistry and electrical engineering.","2026/02/UPCE.png"),
 ("UJEP Ústí nad Labem","UJEP","Ústí nad Labem","https://www.ujep.cz","research",True,["design"],"Polovodičová chemie a budování odborných kapacit v regionu. Návrh čipů: biočipy.","Semiconductor chemicals and regional capacity building. Chip design: biochips.",None),
 ("CEITEC","CEITEC","Brno","https://www.ceitec.cz","research",False,[],"Evropské centrum excelence pro nanotechnologie a pokročilé materiály.","European centre of excellence for nanotechnology and advanced materials.",None),
 ("FZÚ AV ČR","FZÚ","Praha","https://www.fzu.cz","research",False,[],"Fyzikální ústav — výzkum polovodičových materiálů a fotoniky.","Institute of Physics — semiconductor materials and photonics research.","2025/01/fzu.webp"),
 ("ÚPT AV ČR (ISI CAS)","ÚPT","Brno","https://www.isibrno.cz","research",False,[],"Ústav přístrojové techniky — elektronová mikroskopie a přesná měření.","Institute of Scientific Instruments — electron microscopy and precision measurement.","2025/01/isi-cas.webp"),
 ("ÚFM AV ČR (IPM)","ÚFM","Brno","https://www.ipm.cz","research",False,[],"Ústav fyziky materiálů — vlastnosti a spolehlivost materiálů.","Institute of Physics of Materials — material properties and reliability.","2025/01/ipm.webp"),
 ("ÚFE AV ČR","ÚFE","Praha","https://www.ufe.cz","research",False,[],"Ústav fotoniky a elektroniky — fotonika, optické vlákna a senzory.","Institute of Photonics and Electronics — photonics, optical fibres and sensors.","2026/05/ufe.webp"),
 ("Ústav J. Heyrovského AV ČR","ÚFCH JH","Praha","https://www.jh-inst.cas.cz","research",False,[],"Fyzikální chemie povrchů a nanomateriálů.","Physical chemistry of surfaces and nanomaterials.","2025/04/J.-Heyrovsky-Institute-of-Physical-Chemistry.webp"),
 # 08 eco
 ("CyberSecurityHub","CyberSecurityHub","Brno","https://www.cybersecurityhub.cz","eco",False,[],"Kompetenční centrum kyberbezpečnosti pro čipy a kritickou infrastrukturu.","Cybersecurity competence centre for chips and critical infrastructure.","2025/01/cyber_security_hub.webp"),
 ("ICUK","ICUK","Ústí nad Labem","https://www.icuk.cz","eco",False,[],"Inovační centrum Ústeckého kraje — podpora startupů a transferu technologií.","Innovation Centre of the Ústí Region — startup support and technology transfer.","2025/01/icuk.png"),
 ("Zlínský kraj","Zlínský kraj","Zlín","https://www.zlinskykraj.cz","eco",False,[],"Regionální partner rozvoje polovodičového průmyslu v CZ Silicon Valley.","Regional partner for semiconductor industry development in CZ Silicon Valley.","2025/01/zlinreg.webp"),
 ("RHK Brno","RHK Brno","Brno","https://www.rhkbrno.cz","eco",False,[],"Regionální hospodářská komora — služby pro firmy a mezinárodní spolupráci.","Regional Chamber of Commerce — business services and international cooperation.","2025/01/rchk.webp"),
]

NOTES = {
 "UJEP Ústí nad Labem": "v katalogu 8/2026, na semicz.cz/memberlist 18. 10. 2026 chybí – ověřit členství",
 "Advacam": "na semicz.cz/memberlist 18. 10. 2026, v katalogu 8/2026 chybí – doplněno",
}

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

out = []
for n, short, city, url, seg, acad, partner, cs, en, logo in M:
    out.append({"id": slug(short), "n": n, "short": short, "city": city, "url": url, "s": seg,
                "acadChip": acad, "partnerIn": partner, "cs": cs, "en": en,
                "logo": (LG + logo) if logo else "", "li": "", "note": NOTES.get(n, "")})
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
p = os.path.join(os.path.dirname(__file__), '..', 'data', 'members.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'members ->', p)
from collections import Counter
print(Counter(m['s'] for m in out))
