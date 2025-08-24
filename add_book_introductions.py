#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Dictionary of book introductions
BOOK_INTRODUCTIONS = {
    "19_psalms": """The Psalms are a collection of 150 prayers, songs, and poems that express the full range of human emotion in relationship with God. Written by various authors including David, Asaph, and the sons of Korah, they were used in temple worship and personal devotion. The psalms teach us how to pray through praise, lament, thanksgiving, and wisdom, showing that every human experience can be brought before God.""",
    
    "20_proverbs": """Proverbs is a collection of wise sayings primarily from Solomon that teaches practical wisdom for daily life. Using short, memorable statements, it covers topics like relationships, work, money, speech, and character. The book repeatedly emphasizes that true wisdom begins with respecting Yahweh, and that wise living leads to life while foolishness leads to destruction.""",
    
    "21_ecclesiastes": """Ecclesiastes presents the reflections of "the Teacher" (likely Solomon) on the meaning of life. After exploring every earthly pursuit—wisdom, pleasure, work, and wealth—he concludes that everything "under the sun" is meaningless without God. The book teaches that true satisfaction comes not from human achievement but from fearing God, keeping his commands, and enjoying life as his gift.""",
    
    "22_songofsongs": """The Song of Songs is a poetic celebration of romantic love between a man and a woman. Through vivid imagery and passionate dialogue, it portrays the beauty and power of human love as God designed it. The book affirms that sexual love within marriage is good and holy, a gift from God to be celebrated rather than treated with shame or embarrassment.""",
    
    "23_isaiah": """Isaiah prophesied to Judah during a time of moral decay and political upheaval, warning of coming judgment while offering hope of future restoration. His visions span from his own time through the Babylonian exile to the coming of the Messiah and the new heavens and earth. The book masterfully weaves together themes of God's holiness, human sinfulness, divine judgment, and the promise of salvation through the Suffering Servant.""",
    
    "24_jeremiah": """Jeremiah ministered during Judah's final years before the Babylonian exile, calling the nation to repent while knowing they wouldn't listen. Known as the "weeping prophet," he endured rejection, imprisonment, and persecution for faithfully proclaiming God's message. His prophecies include both the certainty of judgment and the promise of a new covenant, where God would write his law on people's hearts.""",
    
    "25_lamentations": """Lamentations is a collection of five poems mourning the destruction of Jerusalem by Babylon in 586 BC. Written in the style of ancient funeral dirges, these poems express raw grief over the city's devastation while acknowledging that God's judgment was deserved. Yet even in the depths of despair, the book affirms God's faithfulness and mercy, declaring that his compassions never fail.""",
    
    "26_ezekiel": """Ezekiel prophesied to the Jewish exiles in Babylon, using dramatic visions and symbolic acts to communicate God's messages. He explained why Jerusalem fell (due to idolatry and injustice), proclaimed judgment on surrounding nations, and offered hope of restoration. His visions include the valley of dry bones coming to life and a new temple with God's glory returning to dwell among his people.""",
    
    "28_hosea": """Hosea's marriage to an unfaithful wife becomes a living parable of God's relationship with Israel. Despite Israel's spiritual adultery through idolatry and injustice, God continues to love his people with steadfast covenant love. The book alternates between judgment and restoration, showing that God's discipline aims to bring his wayward people back to himself.""",
    
    "30_amos": """Amos, a shepherd from Judah, prophesied against Israel during a time of prosperity and complacency. He condemned the nation's social injustice, religious hypocrisy, and oppression of the poor, warning that their wealth and religious rituals couldn't save them from coming judgment. The book emphasizes that true religion requires justice and righteousness, not just religious observance.""",
    
    "31_obadiah": """Obadiah, the shortest book in the Old Testament, pronounces judgment on Edom for their violence against Judah during the Babylonian invasion. The Edomites, descendants of Esau, had gloated over Jerusalem's destruction and even helped capture fleeing refugees. The book demonstrates that God judges nations for their pride and cruelty, and that ultimately his kingdom will prevail.""",
    
    "32_jonah": """Jonah tells the story of a reluctant prophet who tries to flee from God's call to preach to Nineveh, Israel's enemy. After being swallowed by a great fish and given a second chance, Jonah obeys but becomes angry when God shows mercy to the repentant city. The book reveals God's compassion for all nations and challenges narrow nationalism and prejudice.""",
    
    "33_micah": """Micah prophesied to both Israel and Judah, denouncing social injustice, corrupt leadership, and false religion. He predicted the fall of both kingdoms but also promised future restoration under a ruler from Bethlehem. The book famously summarizes true religion: to act justly, love mercy, and walk humbly with God.""",
    
    "34_nahum": """Nahum prophesies the destruction of Nineveh, the capital of the brutal Assyrian Empire that had terrorized the ancient world. Unlike in Jonah's time, the city would not repent and escape judgment. The book demonstrates that while God is slow to anger, he will ultimately judge evil and vindicate his people.""",
    
    "35_habakkuk": """Habakkuk wrestles with the problem of evil, questioning why God allows injustice to continue and why he would use wicked Babylon to punish Judah. God reveals that he will ultimately judge all evil, and that the righteous must live by faith while waiting for God's justice. The book ends with Habakkuk's prayer of trust despite circumstances.""",
    
    "36_zephaniah": """Zephaniah warns of the approaching "day of Yahweh," when God will judge both Judah and the nations for their sin. Yet beyond judgment lies hope: God will purify a remnant who will humbly serve him. The book concludes with a beautiful picture of God rejoicing over his restored people with singing.""",
    
    "37_haggai": """Haggai prophesied to the returned exiles who had become discouraged in rebuilding the temple. He challenged them to put God first, promising that obedience would bring blessing. Though the new temple seemed insignificant compared to Solomon's, Haggai declared that its glory would exceed the former because the Messiah himself would enter it.""",
    
    "38_zechariah": """Zechariah encouraged the returned exiles through visions and prophecies that span from their immediate situation to the distant future. His eight night visions assured them of God's presence and protection. The book contains numerous messianic prophecies, including the coming of the humble king riding on a donkey and the piercing of the one they would mourn.""",
    
    "39_malachi": """Malachi confronts the spiritual apathy of the post-exilic community, who were going through religious motions without genuine devotion. He exposes their sins—corrupt worship, broken covenants, and social injustice—while promising that God would send a messenger to prepare the way for the Lord's coming. The book bridges the Old and New Testaments with its promise of Elijah's return."""
}

def add_introduction_to_book(file_path, introduction):
    """Add an introduction to a book file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if introduction already exists
    if '<div type="introduction">' in content:
        print(f"  Introduction already exists, skipping")
        return
    
    # Find the position after the title
    pattern = r'(<title type="main">[^<]+</title>\s*)'
    match = re.search(pattern, content)
    
    if not match:
        print(f"  WARNING: Could not find title element")
        return
    
    # Create the introduction div
    intro_div = f"""
      <div type="introduction">
        <p>{introduction}</p>
      </div>
      """
    
    # Insert the introduction after the title
    new_content = content[:match.end()] + intro_div + content[match.end():]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Added introduction")

def main():
    """Process all books that need introductions"""
    for book_key, introduction in BOOK_INTRODUCTIONS.items():
        file_path = Path("output") / f"{book_key}_vbt.osis.xml"
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
        
        print(f"Processing {book_key}...")
        add_introduction_to_book(file_path, introduction)
        print(f"Completed {book_key}")
    
    print("\nAll book introductions have been added!")

if __name__ == "__main__":
    main()