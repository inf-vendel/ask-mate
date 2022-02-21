<<<<<<< HEAD
# AskMate (sprint 3)

## Story

Last week you made great progress improving your web application.
We need some more features to make it more usable and more appealing to users.

The users requested new features, such as the ability to register and login.
There are a few other feature requests which you can find in the user stories.

The management wants you to separate the already working features from
the upcoming ones, so your development team need to **start using branching
workflow and open new branches for the features you start in this sprint**.
Just like last week, the ownership is in your hands. There are no compulsory stories,
but of course, management would prefer if all stories were implemented.
So first, choose the stories, then ask a mentor to validate your choice.

Just like last week, you have a **prioritized list** of new user stories that you should
add to the unfinished stories from last week on your product backlog. Try to
estimate these new stories as well, and, based on the estimations, decide how many
your team can finish until the demo. As the order is important, you choose
from the beginning of the list as much as you can.

## What are you going to learn?

- Web routing and redirects
- Gitflow workflow
- Advanced SQL commands (`JOIN`, `GROUP BY`, and aggregate functions)
- User authentication with sessions
- Hashed passwords
- HTML and the Jinja2 templating engine
- Javascript basics DOM manipulation

## Tasks

1. Since you work in a new repository, but also need the code from the previous sprint, add the `ask-mate-3` repository as a new remote to the repository of the previous sprint, then pull (merge) and push your changes into it.
    - There is a merge commit in the project repository that contains code from the previous sprint.

2. As a user, I would like to be able to register a new account in the system.
    - There is a `/registration` page.
    - The page is linked from the front page.
    - There is a form on the `/registration` page when a request is issued with the `GET` method.
    - The form ask for a username (or email address) and a password, then issues a `POST` request to `/registration` on submitting.
    - After submitting, the page redirects to the main page and the new user account is saved in the database.
    - A user account consists of an email address stored as a username, a password stored as a password hash, and a registration date.

3. As a registered user, I would like to be able to log in to the system with my previously saved username and password.
    - There is a `/login` page.
    - The page is linked from the front page.
    - Theres is a form on the `/login` page when a request is issued with `GET` method.
    - The form asks for the username (email address) and password, then issues a `POST` request to `/login` on submit.
    - After submitting the page redirects to the main page and the user is logged in.
    - It is only possible to ask or answer a question when logged in.

4. There should be a page where I can list all the registered users with all their attributes.
    - There is a `/users` page.
    - The page is linked from the front page when logged in.
    - The page is not accessible without logging in.
    - Theres is a `<table>` with user data in it. The table contains the following details of a user.
  - Username (with a link to the user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)

5. As a user, when I add a new question, I would like to be saved as the user who created the new question.
    - The user ID of the logged in user is saved when a new question is added.

6. As a user, when I add a new answer, I would like to be saved as the user who created the new answer.
    - The user ID of the logged in user is saved when a new answer is added.

7. As a user, when I add a new comment, I would like to be saved as the user who created the new comment.
    - The user ID of the logged in user is saved when a new comment is added.

8. There should be a page where we can see all details and activities of a user.
    - There is a `/user/<user_id>` page.
    - The user page of a logged in user is linked from the front page.
    - The page of every user is linked from the users list page.
    - Theres is a list with the following deatils about the user.
  - User ID
  - Username (link to user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)
    - There is a separate table where every **question** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **answer** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **comment** is listed that the user created. The related question is linked in every line.

9. As a user, I would like to have the possibility to mark an answer as accepted.
    - There is a clickable element for every answer on the question page, that can be used for marking an answer as accepted.
    - There is an option to remove the accepted state from an answer.
    - Only the user who asked the question can change the accepted state of answers.
    - An accepted answer has some visual distinction from other answers.

10. As a user, I would like to see a reputation system to strengthen the community. Reputation is a rough measurement of how much the community trusts a user.
    - **A user gains reputation when:**
- their question is voted up: +5
- their answer is voted up: +10
- their answer is marked "accepted": +15

11. As a user, I would like to see a small drop in reputation when a user's question or answer is voted down.
    - **A user loses reputation when:**
- their question is voted down: −2
- their answer is voted down: −2

12. As a user, I would like to see a page that lists all existing tags and the number of questions marked with those tags.
    - There is a `/tags` page.
    - The page is linked from the front page and a question page.
    - The page is accessible whithout logging in.

13. When the user navigates to the `bonus-questions` route and types in the input box, the displayed questions are filtered to match the criteria. This must be done without page reload.
    - When typing `life`, the only question displayed is the one titled `What is the meaning of life ?`.
    - When typing `!life`, questions are filtered to the ones that do NOT include the word `life`. (That is nine questions in this scenario.)
    - When typing `Description:life`, questions are filtered to those that include the word `life` in the `Description` column. (No question is displayed in this scenario.)
    - When typing `!Description:life`, questions are filtered to those that do NOT include the word `life` in the `Description column. (All ten questions are displayed in this scenario)

14. When the user navigates to the `bonus-questions` route and clicks on any table header, the items are sorted based on the column. This must be done without page reload.
    - When clicking the `Description` column, the questions are sorted in alphabetical order, based on the values from the `Description` column.
    - When clicking the `Description` column a second time, the questions are sorted in reverse alphabetical order, based on the values from the `Description` column.

15. [OPTIONAL] When the user navigates to the `bonus-questions` and clicks the `Decrease page font` or `Increase page font` button, the font size is decreased or increased in the page, respectively. This must be done without page reload.
    - Clicking the `Increase page font` button increases the font in the page.
    - Clicking the `Increase page font` button multiple times increases the font size to a maximum of 15. Further clicks do not result in an increase.
    - Clicking the `Decrease page font` button decreases the font the page.
    - Clicking the `Decrease page font` button multiple times decreases the font size to a minimum of 3. Further clicks do not result in an decrease.

## General requirements

- Use gitflow workflow in your team projects from now on.

## Hints

- Use the `CREATE` and `ALTER TABLE` statements to extend and change the database. For more information, see
  [this link](https://www.w3schools.com/sql/sql_alter.asp).
  (Do not forget to set up the foreign keys if you need them.)
- Use one of the following methods to add a value to the timestamp column of a database.
    - Use strings in the following format `'1999-01-08 04:05:06'`,
    - Pass a `datetime` object to the SQL query as a parameter if you use `psycopg2` and the `datetime` module. For more information on date and time handling in psycopg2, see the Background section.
- Insert data into the tables in the appropriate order to avoid violating foreign
key constraints (for example, if you insert data into the `question_tag` before inserting
  the corresponding tag ID in the tag table, the tag you refer to does not exist yet).
  This is especially important after changing the database structure with new foreign keys.
  Consider modifying the sample data based on your changes.
- Optimize your previous queries by applying your knowledge of complex queries and joined tables.
- Remeber that some user stories have prerequisites.
=======
# AskMate (sprint 2)

## Story

Last week you created a pretty good site from scratch. It already has some features but it's a bit difficult to maintain due to the fact that the data is stored in CSV files. Some new features are also needed, to make the site more usable and more appealing to users.

The management decided to move further as users requested new features, such as the ability to comment on answers and tag questions (and of course the issue with CSV files). There are several other feature requests which you can find in the user stories.

Just like last week, management is handing out a **prioritized list** of new user stories that you must add to the unfinished stories from last week on your product backlog. Try to estimate these new stories as well, and, based on the estimations, decide how many of them your team can finish until the demo. As the order is important, you must choose from the beginning of the list as much as you can.

## What are you going to learn?

- Use `psycopg2` to connect to a PostgreSQL database from Python.
- Understand basic SQL commands (`SELECT`, `UPDATE`, `DELETE`, `INSERT`).
- Understand CSS basics.
- Work according to the Scrum framework,
- Create a _sprint plan_.

## Tasks

1. Since you work in a new repository, but also need the code from the previous sprint, add the `ask-mate-2` repository as a new remote to the repository of the previous sprint, then pull (merge) and push your changes into it.
    - There is a merge commit in the project repository that contains code from the previous sprint.

2. Make the application use a database instead of CSV files.
    - The application uses a PostgreSQL database instead of CSV files.
    - The application respects the `PSQL_USER_NAME`, `PSQL_PASSWORD`, `PSQL_HOST` and `PSQL_DB_NAME` environment variables.
    - The database structure (tables) is the same as in the provided SQL file (`sample_data/askmatepart2-sample-data.sql`).

3. Allow the user to add comments to a question.
    - There is a `/question/<question_id>/new-comment` page.
    - The page is linked from the question page.
    - There is a form with a `message` field, and it issues `POST` requests.
    - After submitting, the page redirects to the question detail page, and the new comment appears together with its submission time.

4. Allow the user to add comments to an answer.
    - There is a `/answer/<answer_id>/new-comment` page.
    - The page is linked from the question page, next to or below the answer.
    - There is a form with a `message` field, and it issues `POST` requests.
    - After submitting, the page redirects to the question detail page, and the new comment appears together with its submission time.

5. Implement searching in questions and answers. (Hint: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser))

    - There is a search box and "Search" button on the main page.
    - When writing something and pressing the button, a results list of questions is displayed (with the same data as in the list page).
    - The results list contains questions for which the title or description contain the searched phrase.
    - The results list also contains questions which have answers for which the message contains the searched phrase.
    - The results list URL is `/search?q=<search phrase>`.

6. Allow the user to edit the posted answers.
    - There is a `/answer/<answer_id>/edit` page.
    - The page is linked from the answer page.
    - There is a form with a `message` field, and it issues a `POST` request.
    - The field is pre-filled with existing answer data.
    - After submitting, the page redirects to the question detail page, and the answer is updated.

7. Allow the user to edit comments.
    - The page URL is `/comment/<comment_id>/edit`.
    - There is a link to the edit page next to each comment.
    - The page contains a `POST` form with a `message` field.
    - The field pre-filled with current comment message.
    - After submitting, the page redirects to the question detail page, and the new comment appears.
    - The submission time is updated.
    - There is a message that says "Edited `<number_of_editions>` times." next to or below the comment.

8. Allow the user to delete comments.
    - There is a recycle bin icon next to the comment.
    - Clicking the icon asks the user to confirm the deletion.
    - The deletion itself is implemented by the `/comments/<comment_id>/delete` endpoint (which does not ask for confirmation anymore).
    - After deleting, the page redirects to the question detail page, and the comment is not shown anymore.

9. Display five latest questions on the main page (`/`).
    - The main page (`/`) displays the five latest submitted questions.
    - The main page contains a link to all of the questions (`/list`).

10. Implement sorting for the question list. [If you did this user story in the previous sprint, now you only have to rewrite it to use SQL.]
    - The question list can be sorted by title, submission time, message, number of views, and number of votes.
    - The list can be sorted in ascending and descending order.
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`.

11. Add tags to questions.
    - The tags are displayed on the question detail page.
    - There is an "add tag" link which leads to the page for adding a tag.
    - The URL for the page for adding a tag has is `/question/<question_id>/new-tag`.
    - The page allows to choose from existing tags or define a new one.

12. Highlight the search phrase in the search results.
    - On the search results page, the searched phrase is highlighted.
    - If the phrase is found in an answer, the answer is also displayed (slightly indented).
    - The search phrase is also highlighted in the answers.

13. Allow the user to delete tags from questions.
    - There is an X link next to each tag.
    - Clicking that link deletes the tag and reloads the question page.
    - The deletion is implemented as `/question/<question_id>/tag/<tag_id>/delete` endpoint.

## General requirements

None

## Hints

- It's important that if the database table has a timestamp column then you cannot insert a UNIX timestamp value directly into that table, you should use:
    - either strings in the following format '1999-01-08 04&colon;05&colon;06',
    - or if you use psycopg2 and the datetime module, you can pass a datetime object to the SQL query as parameter (details in the background materials: [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation))
- Pay attention on the order of inserting data into the tables, because you may violate foreign key constraints (that means e.g. if you insert data into the question_tag before you insert into the tag table the corresponding tag id you want to refer to then it won't exist yet)!
- You can import the sample data file into `psql` with the `\i` command or run it via the Database tool in PyCharm.
- Some user stories may require to deal with CSS as well, but do not deal with CSS too much. It's more important that you write proper queries, have a working connection with psycopg2, have a clean Python code than create an amazingly beautiful web application (although if you have time, of course it's not forbidden to do so :smiley:).

### Data models

All data should be persisted in a PostgreSQL database in the following tables (you can ignore data in the not implemented fields):

![AskMate data model part 2](media/web-python/askmate-data-model-part-2.png)

**question table**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The date and time when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* the path to the image for this question<br>

**answer table**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The date and time when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to<br>
*message:* The answer text<br>
*image:* The path to the image for this answer<br>

**tag table**<br>
*id:* A unique identifier for the tag<br>
*name:* The name of the tag<br>

**question_tag table**<br>
*question\_id:* The id of the question the tag belongs to<br>
*tag\_id:* The id of the tag belongs to the question<br>

**comment table**<br>
*id:* A unique identifier for the comment<br>
*question\_id:* The id of the question this comment belongs to (if the comment belongs to an answer, the value of this field should be NULL)<br>
*answer\_id:* The id of the answer this comment belongs to (if the comment belongs to a question, the value of this field should be NULL)<br>
*message:* The comment text<br>
*submission\_time:* The date and time the comment was posted or updated<br>
*edited\_number::* How many times this comment was edited<br>

### Database and sample data

To init the database use the `sample_data/askmatepart2-sample-data.sql` file in your repository.
>>>>>>> askmate2/new_start

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

<<<<<<< HEAD
- <i class="far fa-exclamation"></i> [Working with more complex data](project/curriculum/materials/pages/sql/sql-working-with-data.md)
- [SQL injection](project/curriculum/materials/pages/web-security/sql-injection.md)
- [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
=======
- <i class="far fa-exclamation"></i> [Installing and setting up PostgreSQL](project/curriculum/materials/pages/tools/installing-postgresql.md)
- <i class="far fa-exclamation"></i> [Installing psycopg2](project/curriculum/materials/pages/tools/installing-psycopg2.md)
- <i class="far fa-exclamation"></i> [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Setting up a database connection in PyCharm](project/curriculum/materials/pages/tools/pycharm-database.md)
>>>>>>> askmate2/new_start
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)

<<<<<<< HEAD
### Workflow

- <i class="far fa-exclamation"></i> [Gitflow workflow](project/curriculum/materials/pages/git/git-branching.md)

### Web basics (Sessions/Flask)

- <i class="far fa-exclamation"></i> [Sessions](project/curriculum/materials/pages/web/authentication-sessions.md)
- <i class="far fa-exclamation"></i> [Salted password hashing](project/curriculum/materials/pages/web-security/salted-password-hashing.md)
- <i class="far fa-exclamation"></i> [Flask documentation](http://flask.palletsprojects.com/) (especially the quickstart#the-request-object and quickstart#sessions part)
- [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- <i class="far fa-book-open"></i> [HTTP is stateless](project/curriculum/materials/pages/web/authentication-http-stateless.md)
- <i class="far fa-book-open"></i> [Cookies](project/curriculum/materials/pages/web/authentication-cookies.md)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- <i class="far fa-book-open"></i> [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
=======
### Agile/SCRUM

- [Agile project management](project/curriculum/materials/pages/methodology/agile-project-management.md)
- <i class="far fa-book-open"></i> [Planning poker](https://en.wikipedia.org/wiki/Planning_poker)

### Web basics (Flask/Jinja/HTML/CSS)

- <i class="far fa-exclamation"></i> [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- <i class="far fa-exclamation"></i> [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
- <i class="far fa-book-open"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-book-open"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
>>>>>>> askmate2/new_start
