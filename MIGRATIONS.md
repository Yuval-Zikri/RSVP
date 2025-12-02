# מדריך לניהול שינויים בבסיס הנתונים (Migrations)

הפרויקט משתמש ב-`Flask-Migrate` (מבוסס על Alembic) לניהול שינויים במבנה בסיס הנתונים.

## פקודות נפוצות

כל הפקודות צריכות לרוץ מתוך הקונטיינר של ה-backend או דרך `docker-compose exec`.

### 1. יצירת מיגרציה חדשה
אחרי שביצעת שינויים ב-`models.py` (למשל הוספת עמודה), הרץ את הפקודה הבאה כדי ליצור קובץ מיגרציה:

```bash
docker-compose exec backend flask db migrate -m "תיאור השינוי"
```
למשל:
```bash
docker-compose exec backend flask db migrate -m "add email_background_url to events"
```

### 2. החלת שינויים (Upgrade)
כדי לעדכן את בסיס הנתונים בפועל (להריץ את המיגרציה):

```bash
docker-compose exec backend flask db upgrade
```
*הערה: הקונטיינר מריץ פקודה זו אוטומטית כשהוא עולה.*

### 3. ביטול שינויים (Downgrade)
אם צריך לחזור אחורה:

```bash
docker-compose exec backend flask db downgrade
```

## אתחול ראשוני (חד פעמי)

אם אתה מתקין את הפרויקט מאפס ואין תיקיית `migrations`:

```bash
docker-compose exec backend flask db init
```

## פתרון בעיות

### הטבלה קיימת אבל המיגרציה נכשלת
אם בסיס הנתונים כבר מכיל טבלאות אבל המיגרציות לא מסונכרנות, ניתן "לזייף" מיגרציה או למחוק את המיגרציות ולהתחיל מחדש (בסביבת פיתוח).

### איפוס מלא (זהירות - מוחק נתונים!)
```bash
docker-compose down -v
docker-compose up --build
```
זה ימחק את ה-Volume של הדאטהבייס וייצור הכל מחדש נקי.
