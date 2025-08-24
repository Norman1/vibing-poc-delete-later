#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Dictionary of notes to add: {book: {verse_ref: note_text}}
STUDY_NOTES = {
    "01_genesis": {
        "Gen.24.2": "Placing a hand under the thigh (near the genitals) when making an oath connected the promise to future descendants.",
        "Gen.37.34": "Tearing clothes and wearing sackcloth were required mourning rituals, not spontaneous emotional responses.",
        "Gen.38.14": "Sitting at the entrance wearing a veil identified her as a temple prostitute.",
        "Gen.41.42": "Pharaoh's signet ring gave Joseph authority to act with Pharaoh's full power - documents sealed with it carried royal authority."
    },
    "02_exodus": {
        "Exod.3.5": "Removing sandals acknowledged holy ground and showed respect, as shoes carried dirt from common use.",
        "Exod.12.11": "Eating with 'loins girded' means robes tucked into the belt, ready for immediate travel.",
        "Exod.21.6": "Piercing the ear against the doorpost publicly marked someone as a permanent voluntary servant.",
        "Exod.28.30": "Urim and Thummim were physical objects (possibly stones or lots) used to determine God's will, giving yes/no answers.",
        "Exod.29.24": "Wave offering involved lifting the offering toward the altar and back, symbolically presenting it to God."
    },
    "03_leviticus": {
        "Lev.2.13": "Salt in offerings represented preservation and covenant permanence, as salt prevented decay.",
        "Lev.16.8": "The 'scapegoat' (literally 'goat for Azazel') carried sins into the wilderness.",
        "Lev.19.27": "Not trimming beard edges distinguished Israelites from pagan priests who shaped beards for their gods."
    },
    "04_numbers": {
        "Num.5.23": "Writing curses in a book and washing them into water was a ritual ordeal to determine guilt.",
        "Num.15.38": "Blue tassels (tzitzit) on garment corners served as visual reminders of commandments.",
        "Num.21.8": "Bronze serpents on poles were common healing symbols in the ancient Near East.",
        "Num.21.9": "Bronze serpents on poles were common healing symbols in the ancient Near East."
    },
    "05_deuteronomy": {
        "Deut.6.9": "This led to literal mezuzahs - small cases with scripture attached to doorframes.",
        "Deut.22.8": "Flat roofs required parapets because roofs were used as living spaces.",
        "Deut.25.9": "Removing a sandal and spitting publicly shamed someone for refusing levirate marriage duty.",
        "Deut.25.10": "Removing a sandal and spitting publicly shamed someone for refusing levirate marriage duty."
    },
    "06_joshua": {
        "Josh.2.6": "Flax stalks on the roof were being dried for making linen - roofs served as work areas.",
        "Josh.3.15": "The Jordan overflows during harvest season (April-May) from Mount Hermon's snow melt.",
        "Josh.7.6": "Putting dust on the head was a standard mourning practice."
    },
    "07_judges": {
        "Judg.7.16": "Clay jars hid torch light until broken simultaneously - an ancient flash-bang surprise attack.",
        "Judg.14.12": "Wedding feasts lasted seven days with riddles and entertainment expected from the groom.",
        "Judg.16.13": "Weaving hair into a loom's fabric would make it impossible to remove without cutting.",
        "Judg.16.14": "Weaving hair into a loom's fabric would make it impossible to remove without cutting."
    },
    "08_ruth": {
        "Ruth.2.14": "Bread dipped in wine vinegar was the common field worker's lunch.",
        "Ruth.3.9": "'Spread your garment over me' was a marriage proposal formula.",
        "Ruth.4.7": "Removing and giving a sandal finalized property transfers - the sandal represented walking rights on land."
    },
    "09_1samuel": {
        "1Sam.1.24": "Three-year-old children were weaned late by modern standards.",
        "1Sam.9.9": "'Seer' (ro'eh) was the older term for prophet (nabi).",
        "1Sam.17.7": "A weaver's beam was about 2-3 inches (5-8 cm) thick.",
        "1Sam.24.3": "'Cover his feet' is a euphemism for defecation.",
        "1Sam.28.24": "Fatted calves were kept penned and fed grain for special occasions."
    },
    "10_2samuel": {
        "2Sam.1.21": "'No dew or rain' was a curse making land unproductive.",
        "2Sam.12.20": "Anointing oneself ended the mourning period.",
        "2Sam.13.19": "Ashes on head and torn robes signaled both mourning and violation.",
        "2Sam.18.18": "Pillars served as memorial monuments - having no son meant no one to preserve your name."
    },
    "11_1kings": {
        "1Kgs.1.40": "Playing flutes was standard celebration music.",
        "1Kgs.7.26": "A bath measure equaled about 22 liters.",
        "1Kgs.18.28": "Cutting oneself until blood flowed was a pagan practice to get deities' attention."
    },
    "12_2kings": {
        "2Kgs.2.23": "'Baldhead' was a deadly insult possibly referring to leprosy.",
        "2Kgs.5.17": "Two mule-loads of earth - deities were thought tied to their land.",
        "2Kgs.9.13": "Placing garments under someone's feet showed submission.",
        "2Kgs.23.10": "Topheth in the Valley of Hinnom was where children were burned in sacrifice."
    },
    "18_job": {
        "Job.1.20": "Shaving one's head showed mourning - hair represented life and vigor.",
        "Job.2.8": "Pottery shards were used to scrape skin diseases.",
        "Job.7.6": "A weaver's shuttle moves rapidly back and forth.",
        "Job.19.24": "Writing with iron on lead or rock created permanent records.",
        "Job.31.35": "Making one's mark (taw) was signing with an X or personal seal."
    },
    "19_psalms": {
        "Ps.23.5": "Anointing a guest's head with oil was hospitality; overflowing cup showed abundance.",
        "Ps.45.8": "Myrrh, aloes, and cassia were expensive perfumes for wedding garments.",
        "Ps.137.9": "Dashing infants against rocks was standard ancient warfare practice."
    },
    "20_proverbs": {
        "Prov.22.28": "Moving boundary stones was theft - stones marked property lines.",
        "Prov.25.22": "Coals of fire on head refers to Egyptian repentance ritual.",
        "Prov.31.13": "Working with flax and wool meant the complete textile process."
    },
    "21_ecclesiastes": {
        "Eccl.12.6": "Silver cord, golden bowl, pitcher, and wheel are metaphors for body parts failing."
    },
    "23_isaiah": {
        "Isa.1.6": "Oil was primary medicine for wounds.",
        "Isa.3.16": "Tinkling anklets described wealthy women's affected walk.",
        "Isa.20.2": "Prophets sometimes acted out messages physically.",
        "Isa.20.3": "Prophets sometimes acted out messages physically.",
        "Isa.30.14": "Pottery shards had many uses - carrying coals or dipping water."
    },
    "24_jeremiah": {
        "Jer.19.1": "The Potsherd Gate led to the pottery dump.",
        "Jer.19.2": "The Potsherd Gate led to the pottery dump.",
        "Jer.32.14": "Documents in clay jars could last centuries.",
        "Jer.36.23": "Scrolls were read column by column."
    },
    "25_lamentations": {
        "Lam.2.10": "Elders sitting on ground in silence with dust on heads showed corporate mourning.",
        "Lam.4.2": "Comparing people to clay pots meant they were common and easily replaced."
    },
    "26_ezekiel": {
        "Ezek.4.9": "Mixing different grains made famine bread - normally kept separate.",
        "Ezek.4.10": "Mixing different grains made famine bread - normally kept separate.",
        "Ezek.5.1": "Using a sword as a razor symbolized military judgment.",
        "Ezek.13.18": "Magic bands and veils were fortune-telling accessories."
    },
    "27_daniel": {
        "Dan.1.12": "'Vegetables' meant food from seeds - grains and legumes included.",
        "Dan.5.29": "Purple clothing indicated royal status from expensive murex dye."
    },
    "40_matthew": {
        "Matt.3.12": "Winnowing fork tossed grain in air for wind to separate chaff.",
        "Matt.4.5": "Temple pinnacle was southeast corner with 140-meter drop.",
        "Matt.5.41": "Roman soldiers could legally force civilians to carry equipment one mile.",
        "Matt.9.17": "New wine expands during fermentation, bursting old inflexible wineskins.",
        "Matt.23.5": "Phylacteries were small leather boxes with scripture worn during prayer.",
        "Matt.25.1": "Wedding processions occurred at night, requiring lamps.",
        "Matt.27.48": "Sour wine (posca) was cheap diluted wine for soldiers and laborers."
    },
    "41_mark": {
        "Mark.2.4": "Palestinian roofs were flat, made of branches and mud, easily opened.",
        "Mark.5.20": "Decapolis was a league of ten Greek cities with special autonomy.",
        "Mark.7.11": "'Corban' meant dedicated to God - preventing other use."
    },
    "42_luke": {
        "Luke.2.7": "A manger was an animal feeding trough, often carved from stone.",
        "Luke.10.34": "Oil soothed wounds; wine's alcohol was antiseptic.",
        "Luke.11.5": "Midnight bread request implies unexpected guest creating hospitality emergency."
    },
    "43_john": {
        "John.2.6": "Stone jars holding 75-115 liters each were for ritual purification.",
        "John.4.9": "Sharing vessels with Samaritans made Jews ritually unclean.",
        "John.9.7": "Pool of Siloam received water through Hezekiah's tunnel from Gihon Spring.",
        "John.11.44": "Burial wrappings included strips around body and separate face cloth.",
        "John.13.23": "Reclining at meals meant lying on left side - the beloved disciple was in front of Jesus.",
        "John.18.28": "Entering Gentile buildings made Jews ritually unclean for Passover.",
        "John.19.31": "Bodies on crosses during Sabbath violated Deuteronomy 21:23."
    },
    "44_acts": {
        "Acts.1.12": "Sabbath day's journey was 2,000 cubits (about 900 meters).",
        "Acts.9.43": "Tanning was unclean work; tanners lived outside towns.",
        "Acts.10.6": "Tanners needed water and isolation due to smell.",
        "Acts.17.18": "Epicureans sought happiness through pleasure; Stoics through emotionless virtue.",
        "Acts.21.38": "Sicarii were Jewish revolutionaries with concealed daggers.",
        "Acts.27.9": "The Fast (Day of Atonement) marked dangerous sailing season."
    },
    "45_romans": {
        "Rom.16.23": "City treasurer (oikonomos) was high civic office."
    },
    "46_1corinthians": {
        "1Cor.7.36": "Past marriageable age meant early teens in that culture.",
        "1Cor.8.10": "Temple dining rooms were central to civic and business life.",
        "1Cor.9.24": "Isthmian Games near Corinth made athletic metaphors meaningful.",
        "1Cor.16.22": "Maranatha is Aramaic for 'Our Lord, come!'"
    },
    "47_2corinthians": {
        "2Cor.2.14": "Triumphal processions displayed conquered enemies for execution.",
        "2Cor.11.24": "Thirty-nine lashes avoided accidentally exceeding the forty-lash limit."
    },
    "48_galatians": {
        "Gal.3.24": "A pedagogue was a slave supervising children, not a teacher."
    },
    "49_ephesians": {
        "Eph.6.16": "Fiery darts were arrows wrapped in burning pitch-soaked cloth."
    },
    "50_philippians": {
        "Phil.3.2": "'Dogs' was a Jewish insult for Gentiles."
    },
    "52_1thessalonians": {
        "1Thess.5.26": "Holy kiss was standard same-gender greeting."
    },
    "54_1timothy": {
        "1Tim.2.9": "Elaborate braided hair with gold displayed wealth and took hours."
    },
    "58_hebrews": {
        "Heb.9.19": "Hyssop was a bushy plant used as a brush for sprinkling.",
        "Heb.12.16": "Birthright included double inheritance and family leadership."
    },
    "59_james": {
        "James.2.2": "Gold ring indicated equestrian or senatorial rank."
    },
    "60_1peter": {
        "1Pet.3.3": "Elaborate hairstyles required hours of skilled slave work."
    },
    "61_2peter": {
        "2Pet.2.22": "Dogs and pigs returning to filth were proverbs about unchangeable nature."
    },
    "66_revelation": {
        "Rev.2.17": "White stones were admission tickets or acquittal votes.",
        "Rev.3.18": "Laodicea's black wool and eye salve industries make the imagery pointed.",
        "Rev.6.6": "A denarius for a quart of wheat meant subsistence living.",
        "Rev.16.16": "Armageddon (Har-Megiddo) was a valley of many ancient battles."
    }
}

def add_note_to_verse(content, verse_ref, note_text):
    """Add a background note to a specific verse"""
    # Pattern to find the verse
    pattern = f'<verse osisID="{verse_ref}">([^<]*)</verse>'
    
    # Check if note already exists
    if f'<note type="background">' in content and verse_ref in content:
        print(f"  Note already exists for {verse_ref}, skipping")
        return content
    
    # Replace with verse + note
    replacement = f'<verse osisID="{verse_ref}">\\1<note type="background">{note_text}</note></verse>'
    
    new_content, count = re.subn(pattern, replacement, content)
    
    if count > 0:
        print(f"  Added note to {verse_ref}")
    else:
        print(f"  WARNING: Could not find {verse_ref}")
    
    return new_content

def process_book(book_file, notes):
    """Process a single book file and add all notes"""
    file_path = Path("output") / f"{book_file}_vbt.osis.xml"
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    print(f"\nProcessing {book_file}...")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add each note
    for verse_ref, note_text in notes.items():
        content = add_note_to_verse(content, verse_ref, note_text)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Completed {book_file}")

def main():
    """Process all books with study notes"""
    for book_file, notes in STUDY_NOTES.items():
        if notes:  # Only process if there are notes
            process_book(book_file, notes)
    
    print("\n✓ All study notes have been added!")

if __name__ == "__main__":
    main()