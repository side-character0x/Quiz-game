# Quiz Master 🎯

A quiz game built with Flask and Python. It fetches real-time questions from the Open Trivia Database (OpenTDB) API, allowing users of the app to test their knowledge among various categories and difficulties provided in the app.

## Features

- **User Authentication:** Authentication system requiring correct pin and username to access the account.New users can register and set their own unique pin and username.
- **Question Fetching:** Fetshes questions from the Open Trivia Database API for larger pool of questions.
- **Multiple Difficulties:** user can choose the difficulty of the questions.
- **Category Selection:** user can choose the category of the question,they will be asked.
- **Coin System:** user can earn specific coins for every correct answer.
- **Hints:** user can use coins to use hints to remove 2 options from the existing 4 options.
- **Rapid Fire Mode:** a mode where you can answer as many questions you can in 30 seconds.[Note: This version only supports limited questions currently.]
- **Game Summaries:** Your game summary will be displayed at the end of the game.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Jinja2
- **External API:** [Open Trivia Database](https://opentdb.com/)

## How to Run (For Reviewers)

**Step 1: Download and Extract**
1. Go to the **Releases** page on the right side of this repository.
2. Download the `QuizMaster.zip` file.
3. Extract (unzip) the folder to a location on your computer.

**Step 2: Run the App**
1. Open the extracted folder.
2. Double-click **`QuizMaster.exe`**.
3. A terminal window will open. The app will start the server and automatically open in your web browser at `http://127.0.0.1:5000`.

*(Note: If Windows Defender SmartScreen blocks the app, click "More info" and then "Run anyway". This is normal for unsigned Python executables).*