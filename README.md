<h1 dir="rtl" align="right">אתר הדגמה ל־Basic Theta*</h1>

<p dir="rtl" align="right">
זהו אתר Flask להדגמת האלגוריתם Basic Theta*. המשתמש יכול להזין גריד בעצמו או ליצור קלט אקראי, ולראות את המסלול, בדיקת קו הראייה והלוגים. באתר יש גם קישור למאמר ודף אודות. אין בו מימוש AP.
</p>

<h2 dir="rtl" align="right">הרצה מקומית</h2>

<p dir="rtl" align="right">אחרי שכפול המאגר, פותחים טרמינל בתיקיית האתר ומריצים:</p>

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe app.py
```

<p dir="rtl" align="right">
האתר נפתח בכתובת <code>http://127.0.0.1:5000</code>. לבדיקות מתקינים גם <code>pytest</code> ומריצים <code>./.venv/Scripts/python.exe -m pytest tests -v</code>. מתוך תיקיית <code>project</code> של הפרויקט המשותף אפשר להריץ גם <code>./start.ps1</code>.
</p>

<h2 dir="rtl" align="right">התקנת האלגוריתם</h2>

<p dir="rtl" align="right">
קובץ <code>requirements.txt</code> מתקין את Basic Theta* מהענף <code>codex/theta-star-deployment</code> ב־fork. הענף הזה מכיל את המימוש וגם הגדרות התקנה קטנות ב־<code>pyproject.toml</code>, כי אי אפשר להתקין את המאגר המקורי ישירות באמצעות pip. כך ה־PR של האלגוריתם נשאר עם קובצי האלגוריתם והבדיקות בלבד. ההתקנה נבדקה מקומית. לפיתוח בלי התקנה אפשר להגדיר את <code>THETA_STAR_REPO</code> לנתיב המקור.
</p>

<h2 dir="rtl" align="right">פריסה לשרת המחלקה</h2>

<ol dir="rtl" align="right">
<li>מקבלים מהמחלקה חשבון ופורט בהתאם להוראות העדכניות.</li>
<li>יוצרים בשרת סביבה וירטואלית ומריצים <code>pip install -r requirements.txt</code>.</li>
<li>בודקים שהייבוא <code>from graphs.theta_star import theta_star</code> מצליח.</li>
<li>מריצים <code>gunicorn --workers 1 --bind 127.0.0.1:PORT wsgi:app</code> ומחברים לשירות המחלקה.</li>
<li>בודקים באתר הציבורי קלט רגיל, קלט אקראי, קלט שגוי ולוגים.</li>
</ol>

<p dir="rtl" align="right">
האתר אינו משתמש במסד נתונים או במפתח סודי. גודל הקלט מוגבל ל־50×50, ומצב debug כבוי. הוראות השרת והפורט המדויקים ייקבעו לפי פרטי הגישה מהמחלקה.
</p>
