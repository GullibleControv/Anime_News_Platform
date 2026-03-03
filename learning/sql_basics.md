# SQL Basics for Your Work

You use PostgreSQL at work. This file teaches the SQL you'll encounter daily.

## How to Practice

You can practice SQL with your anime project's SQLite database:

```bash
cd C:\projects\personal\Anime_News_Platform
python manage.py dbshell
```

Or use https://sqlbolt.com for interactive exercises.

---

## The Basics

A database has **tables** (like spreadsheets).
Each table has **rows** (records) and **columns** (fields).

Your `news_article` table looks like:

| id | title | content | category | published_date | image_url |
|----|-------|---------|----------|----------------|-----------|
| 1 | "Anime News" | "Content..." | "NEWS" | 2024-01-01 | "http://..." |
| 2 | "Review" | "Content..." | "REVIEW" | 2024-01-02 | "http://..." |

---

## SELECT - Reading Data

```sql
-- Get all columns from all rows
SELECT * FROM news_article;

-- Get specific columns
SELECT title, category FROM news_article;

-- Get one row by ID
SELECT * FROM news_article WHERE id = 1;

-- Get rows matching a condition
SELECT * FROM news_article WHERE category = 'NEWS';

-- Multiple conditions
SELECT * FROM news_article WHERE category = 'NEWS' AND id > 5;

-- Sort results
SELECT * FROM news_article ORDER BY published_date DESC;

-- Limit results
SELECT * FROM news_article LIMIT 5;

-- Count rows
SELECT COUNT(*) FROM news_article;

-- Count by category
SELECT category, COUNT(*) FROM news_article GROUP BY category;
```

---

## INSERT - Adding Data

```sql
-- Add a new row
INSERT INTO news_article (title, content, category)
VALUES ('New Article', 'Content here', 'NEWS');

-- Add multiple rows
INSERT INTO news_article (title, content, category) VALUES
('Article 1', 'Content 1', 'NEWS'),
('Article 2', 'Content 2', 'REVIEW');
```

---

## UPDATE - Modifying Data

```sql
-- Update one row
UPDATE news_article SET title = 'Updated Title' WHERE id = 1;

-- Update multiple columns
UPDATE news_article SET title = 'New', category = 'REVIEW' WHERE id = 1;

-- Update multiple rows (careful!)
UPDATE news_article SET category = 'NEWS' WHERE category = 'news';
```

**WARNING:** Without WHERE, you update ALL rows!

---

## DELETE - Removing Data

```sql
-- Delete one row
DELETE FROM news_article WHERE id = 1;

-- Delete rows matching condition
DELETE FROM news_article WHERE category = 'OLD';
```

**WARNING:** Without WHERE, you delete ALL rows!

---

## Practice Exercises

Try these with your anime database:

### Exercise 1: Basic SELECT
```sql
-- TODO: Get all articles
-- TODO: Get only titles
-- TODO: Get articles with category 'NEWS'
```

### Exercise 2: Counting
```sql
-- TODO: Count total articles
-- TODO: Count articles per category
```

### Exercise 3: Sorting
```sql
-- TODO: Get 5 most recent articles
-- TODO: Get articles sorted by title A-Z
```

### Exercise 4: Filtering
```sql
-- TODO: Get articles where title contains 'anime'
-- Hint: Use LIKE '%anime%'
```

---

## How Django Uses SQL

When you write Django code, it generates SQL:

```python
# Django ORM
Article.objects.all()
# Becomes: SELECT * FROM news_article

# Django ORM
Article.objects.filter(category='NEWS')
# Becomes: SELECT * FROM news_article WHERE category = 'NEWS'

# Django ORM
Article.objects.get(id=1)
# Becomes: SELECT * FROM news_article WHERE id = 1 LIMIT 1
```

Understanding SQL helps you understand what Django is doing!

---

## Common Patterns at Work

### Finding duplicates
```sql
SELECT title, COUNT(*) as count
FROM news_article
GROUP BY title
HAVING COUNT(*) > 1;
```

### Recent items
```sql
SELECT * FROM news_article
ORDER BY published_date DESC
LIMIT 10;
```

### Search
```sql
SELECT * FROM news_article
WHERE title LIKE '%keyword%';
```

### Join tables (when you have users)
```sql
SELECT users.username, articles.title
FROM users
JOIN articles ON users.id = articles.author_id;
```

---

## Key Takeaways

1. `SELECT` = read data
2. `INSERT` = add data
3. `UPDATE` = modify data (always use WHERE!)
4. `DELETE` = remove data (always use WHERE!)
5. `WHERE` = filter which rows
6. `ORDER BY` = sort results
7. `LIMIT` = restrict number of results
8. `COUNT/GROUP BY` = aggregate data

Master these and you'll understand 80% of database work.
