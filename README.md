# אתר הדגמה ל־Basic Theta*

זהו מאגר Git נפרד. האתר מקבל גריד, יוצר גם קלט אקראי, מציג מסלול,
בדיקת קו ראייה, לוגים וקישור למאמר. אין בו מימוש AP.

אחרי שכפול המאגר ל־Windows, מתוך תיקיית האתר:

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe app.py
```

האתר נפתח ב־http://127.0.0.1:5000. לבדיקות מתקינים גם `pytest`
ומריצים `./.venv/Scripts/python.exe -m pytest tests -v`.
בתיקיית הפרויקט המשותפת אפשר פשוט להריץ `./start.ps1` מתוך `project`.

`requirements.txt` מתקין את Basic Theta* מענף Git ייעודי
`codex/theta-star-deployment` ב־fork. הענף הזה זהה לענף המימוש,
בתוספת הגדרות התקנה קטנות ב־`pyproject.toml`: המאגר המקורי אינו
ניתן להתקנת pip ישירות בגלל מבנה התיקיות שלו. כך ענף ה־PR נשאר
עם קובצי האלגוריתם והבדיקות בלבד. ההתקנה נבדקה מקומית.
לפיתוח מקומי בלי התקנה אפשר להגדיר `THETA_STAR_REPO` לנתיב המקור.

פריסה עתידית, לאחר אישור המרצה:

1. ענף הפריסה ומאגר האתר כבר פורסמו; לפני פריסה בודקים שהם מעודכנים.
2. לקבל חשבון ופורט לפי הוראות שרת המחלקה העדכניות.
3. בשרת ליצור venv ולהריץ `pip install -r requirements.txt`.
4. לוודא ש־`python -c "from graphs.theta_star import theta_star"` מצליח.
5. להריץ `gunicorn --workers 1 --bind 127.0.0.1:PORT wsgi:app` ולחבר לשירות המחלקה.
6. לבדוק באתר הציבורי קלט רגיל, אקראי, שגוי ולוגים, ואז לצלם מסכים.

אין באתר database או מפתח סודי; קלט מוגבל ל־50×50 ו־debug כבוי.
הוראות השרת המדויקות והפורט עדיין מחייבים אישור מול המחלקה.
