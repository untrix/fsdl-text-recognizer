# Lab 1 Instructions

## Checking out the repo

Start by cloning the repo (you may already have it present in your home directory), then going into it and pulling the latest version.

```sh
git clone https://github.com/gradescope/fsdl-text-recognizer-project.git
cd fsdl-text-recognizer-project
git pull origin master
```

Now go to https://github.com/gradescope/fsdl-text-recognizer-project and click Fork in the top right.
Select your personal account to fork to, and note down your USERNAME, which will be right after https://github.com in the URL that you will be taken to.
Add your fork as a remote of the repo and push to it

```sh
git remote add mine https://github.com/USERNAME/fsdl-text-recognizer-project.git
git push mine master
```

This should prompt you to enter your Github username and password.
If your password is not accepted, it may be because you have two-factor authentication enabled.
Follow directions here to generate a token you can use instead of your password on the command line: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
Make sure you store the token (e.g. in your password manager)!

## Submitting to Gradescope

Go to https://gradescope.com/courses/21098/assignments and click the lab you want to submit to.
Submit via github: select your fork of the `fsdl-text-recognizer-project` repo and the master branch, and submit.
Don't forget to enter a name for the leaderboard :)

The autograder should finish in <1 min, and display the results.
Your name will show up in the Leaderboard.