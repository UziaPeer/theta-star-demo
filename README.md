<h1 dir="rtl" align="right">אתר הדגמה ל־Basic Theta*</h1>

<p dir="rtl" align="right">
אתר Flask קטן שמדגים מציאת מסלול בעזרת Basic Theta*. אפשר להזין גריד עם מכשולים או ליצור גריד אקראי, ואז לראות את המסלול ואת לוג ההרצה.
</p>

<h2 dir="rtl" align="right">הרצה מקומית</h2>

<p dir="rtl" align="right">אחרי שכפול המאגר, פותחים טרמינל בתיקיית האתר ומריצים:</p>

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe app.py
```

<p dir="rtl" align="right">
האתר נפתח בכתובת <code>http://127.0.0.1:5000</code>. להרצת הבדיקות מתקינים <code>pytest</code> ומריצים <code>./.venv/Scripts/python.exe -m pytest tests -v</code>.
</p>

<h2 dir="rtl" align="right">התאמה לשרת המחלקה</h2>

<p dir="rtl" align="right">
קובץ <code>requirements.txt</code> מקבע את <code>gunicorn==22.0.0</code>, בהתאם למדריך שרת המחלקה. נקודת הכניסה של השירות היא <code>app:app</code>; הקובץ <code>wsgi.py</code> מספק גם את נקודת הכניסה <code>wsgi:app</code> לבדיקה או להפעלה ידנית.
</p>
