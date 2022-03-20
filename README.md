# Notes

## Architecture

- Database: MySQL?
- Logic flow:
  - Fetch feed periodically (hourly? every fifteen min?)
  - Parse feed
  - Match article database (title hash?)
  - Add new article to database
  - Push new article to channel

## Feed
- Database Model
  - ID `id` num
  - Name `name` string
  - URL `url` string
  - Time added (?) 
  - number of articles (?)
  - Tags `tags` list of string

## Article
- Database Model
  - Title `title` string
  - Author `author` string
  - URL `url` string
  - Publication date `pub_date` num
  - ID `id` num (hash of name?)
  - Tags `tags` list of string
  - Feed ID `feed_id` num

  


## Telegram
- Display
  - Title with link
  - Time published
  - Tags
  - Summary(?)
- Inline options: (?)
  - Like: give the feed more weight `Like`
  - Summarize `TLDR`
  - Comments `Comment` (?)