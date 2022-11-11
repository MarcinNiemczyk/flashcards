# Flashcards <a name="introduction"></a>

### Table of Contents
- [Introduction](#introduction)
	- [What is a flashcard?](#what-is-a-flashcard)
	- [How to use it?](#how-to-use-flashcards)
- [Overview](#overview)
	- [✨ Demo](#demo)
	- [🚀 Usage](#usage)
	- [Background](#background)
- [Features](#features)
	- [History Tracker](#history-tracker)
	- [Interactive Flashcards](#interactive-flashcards)
	- [Collections Exchange](#collections-exchange)
	- [Customized Profiles](#customized-profiles)
- [Others](#others)
	- [Tech Stack](#tech-stack)
	- [Authors](#authors)

### What is a flashcard? <a name="what-is-a-flashcard"></a>
A **flashcard** is a card bearing information on both sides, which is intended to be used as an aid in memorization. Each flashcard bears a question on one side and an answer on the other.

### How to use it? <a name="how-to-use-flashcards"></a>
Flashcards exercise the mental process of **active recall**: given a prompt (the question), one produces the answer. 
- It is important to use the flashcards multiple times. 
- One of the most efficient method is Leitner system, which is a simple implementation of the principle of spaced repetition, where cards are reviewed at increasing intervals. [This method of four boxes system is planned for future release]
- Using flashcards can be a very effective self-testing approach.

## Overview <a name="overview"></a>

Project is built as a dynamic website using *Model-View-Template* pattern, where **Django** is utilized as a back-end language, and **JavaScript** on the front-end. Application supports mobile screens as well as desktop ones.

Complexity is provided with 18 endpoints, 426 lines of JavaScript, 11 HTML Templates, 5 database tables and 57 unit tests, which are fully automated **CI/CD** as Github Workflow.


### ✨ Demo <a name="demo"></a>
Demo version currently unavailable. [It will be set up in the future]

Presentation video available here: [https://youtu.be/AbiBgzYQpB4](https://youtu.be/AbiBgzYQpB4)

### 🚀 Usage <a name="usage"></a>
1. Download repository.
	``` 
    git clone <url> 
    ```
2. Install requirements.
	```
    pip install -r requirements.txt
    ```
3. Run application.
	```
    python manage.py runserver
    ```
	Go to ``` 127.0.0.1:8000 ```

### Background <a name="background"></a>
Purpose of this application was to create custom place for flashcards, where I could make it however I want and improve my foreign languages vocabulary. I used to learn from physical flashcards, made by hand from scraps of cardboard, but to save my time I switched to digital ones. After a while I realized that those apps didn't fit my needs and I needed to create it on my own. So this is my version of flashcards.

## Features <a name="features"></a>

#### History Tracker <a name="history-tracker"></a>
Collections, which are sets of flashcards, can be accessed by multiple ways (editing, viewing details, learning etc.). Every interaction with a collection is saved in logs. This offers a few possibilities such as sorting library collections by latest visit, or history view [this view is planned for a future release], where user can easy find his recently viewed collections.

#### Interactive Flashcards <a name="interactive-flashcards"></a>
This is the main feature of this application. Flashcards view, also known as learning view, is developed to resemble physical flashcard. User can flip it with an animation of flipping or switch it to the next one. Latest flashcard index is remembered and stored server side, so the previous session is restored and user can continue learning from that point.

**Settings:** Flashcards have also additional features within settings - randomize, which is changing order of flashcards (Fisher-Yates shuffle algorithm) and reverse - flip all flashcards and answer by task language.

#### Collections Exchange <a name="collections-exchange"></a>
Users can set their collections to public, so they will be visible in explore view by others. They can follow collections to "grab" it from here to their own library and learn. To easy navigate through all shared items, there is a filter with search field and languages select, and explore pages are paginated. 

#### Customized Profiles <a name="customized-profiles"></a>
Profile link is attached in many points, mainly as an author of collection. To distinguish itself user is able to set his profile picture (avatar), which uploaded is overwritten to 128x128 pixels. It is placed next to his username and visible larger on profile page.


## Others <a name="others"></a>

### Tech Stack <a name="tech-stack"></a>
- Django
- JavaScript
- PostgreSQL
- AWS S3
- Bootstrap 5
- HTML
- CSS


### Authors <a name="authors"></a>
 - **[martindustry](https://github.com/martindustry)**


