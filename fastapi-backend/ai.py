import openai
from openai import AsyncOpenAI
import os
import asyncio

#here
#from dotenv import load_dotenv
import json
#here
#load_dotenv()  # ✅ Load from .env file

client = AsyncOpenAI(api_key=os.getenv("OPEN_AI_KEY"))  

async def extract_place_info(text: str) -> dict:
    prompt = f"""
You are a highly accurate assistant that extracts structured data from Instagram Reel captions recommending places to eat or drink. 
You have the **name** of the place so you must find it.
Your task is to analyze the following caption and return a JSON object with the following fields:
- **name**: the name of the place (restaurant, bar, cafe, etc.). This is required — if not found, return "Unknown".
- **city**: the city if mentioned, otherwise "Unknown".
- **address_hint**: street, neighborhood, or market name (e.g., "Rothschild Blvd", "Shuk HaCarmel"). If unknown, return "Unknown".
- **type**: classify the place as one of ["cafe", "restaurant", "bar", "bakery", "market", "other"]. If unsure, use "other".
- **summarize**: a 1-sentence summary of the recommendation, suitable for a tourist visiting that city.
you need to answer in english
Respond **only with a valid JSON object** like this:
{{
  "name": "Cafe Europa",
  "city": "Tel Aviv",
  "address_hint": "Rothschild Boulevard",
  "type": "cafe",
  "summarize": "A stylish cafe in central Tel Aviv offering great coffee and pastries."
}}

Text to analyze:
\"\"\"{text}\"\"\"
"""

    response = await client.chat.completions.create(
        model="gpt-4.1-nano",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise ValueError(f"Failed to parse response: {e}")
#from her eput all in comment
# ----------------------------------------
# TESTING CODE (safe to leave as comment)
# ----------------------------------------
   #write main function to test the code
#if __name__ == "__main__":
    
    #text1 = "ni and Food | בלוגרית אוכל | יוצרת תוכן | המלצות למסעדות‏ באינסטגרם ‏בית קפה יפני עם אוניגירי בעבודת יד🥢 הכירו את איקארי , עסק קטן ומשפחתי של מנאמי אונו. היא מוכרת שם אוניגירי בעבודת יד, ראמן, מאצ׳ה וקינוחים יפניים. מקום סופר מקסים בשוק הכרמל! פרטים נוספים: •אין תעודת כשרות. •כתובת- מל״ן 39, שוק הכרמל ת״א. •יש אופציות לטבעונים וללא גלוטן🌱 •ימים ושעות פעילות: א׳-ב׳ | 08:30-16:00 | אין ראמן ג׳-ה׳ | 08:30-22:00 | יש ראמן החל מ16:00 ו׳ | 08:30-16:00 | יש ראמן החל מ11:00 איקארי - @okasancafetlv‏‎"
    #Example usage
    
    text2 = """
Oysters for a euro? You don’t have to tell us twice 🤩🦪
Helena is a stylish wine bar next to the Habima Theater, serving Spanish-inspired tapas and an excellent imported wine selection, and from Sunday to Thursday between 18:00-19:00, they offer Oyster Hour – where each oyster is just 1 euro (4₪)! 🔥
In the reel you can see their oysters (obviously), bread and butter, jamón and melon, hard cheese with honey, a bottle of wine, and chocolate mousse 🍷
אויסטרים ביורו? לא צריך להגיד לנו פעמיים 🤩🦪
הלנה הוא בר יין מעוצב שנמצא ממש ליד תיאטרון הבימה ומגיש טאפאסים באווירה ספרדית ומבחר מעולה של יינות מיובאים, ומראשון עד חמישי בין 18:00 ל19:00 הם מציעים אויסטר האוור שבה כל אויסטר עולה רק יורו אחד (4₪)! 🔥
בריל תוכלו לראות את האויסטרים (כמובן), לחם וחמאה, חמון ומלון, גבינה קשה עם דבש, בקבוק יין ומוס שוקולד 🍷
.
.
4₪ per oyster during Oyster Hour, 19₪ for the bread and butter, 65₪ for the Jamón and melon, 42₪ for the Hard cheese and honey, 285₪ for the bottle of wine, and 41₪ for the chocolate mousse"""
    text = """מקום חדש של בייגלים אמריקאיים אורגינלללל🥯

ולא סתם מקום, מקום של מיכל אפשטיין.
זו אחת הנשים שאני הכי תופסת מהן בתחום האוכל,
לפני שהגעתי ידעתי שזה מסוג המקומות שאני יאהב וגם אחזור לשם בטוח!

הבייגלים עצמם חלומיים, הם במתכון של מיכל ומכינים אותם שם כל יום מ0.

המחירים נעים בין 26-66₪ תלוי בתוספות,
הם פתחו היום והם בהרצה אז הכל לוקח קצת זמן אז קחו בחשבון🫶🏼

אני עפתיייייי ממליצה ממש,
📍שמירז, בן יהודה 171 תל אביב
@schmearz_bagels
"""
    #result = asyncio.run(extract_place_info(text))
   # print(json.dumps(result, indent=2, ensure_ascii=False))