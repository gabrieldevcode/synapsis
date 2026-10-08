# Synapsis

A spaced-repetition study manager that runs entirely in the terminal, in pure
Python, with nothing to install besides Python itself.

Synapsis keeps track of what you studied, measures how well you master each
subject and uses that to build a review queue, instead of leaving the "what
should I review today?" decision to your memory, which is exactly the part
that is failing.

This is the final project for the **Computer Science 1** course.

> **Privacy:** the `users/` folder, where profiles and all registered content
> live, is **not** part of this repository: it is in `.gitignore`. A fresh
> clone ships with no student data at all. To see the program working with
> content, there is a fictional user generator, described in
> [Quick start](#-quick-start).

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)

---

## Contents

- [The problem](#-the-problem)
- [How it works, at a glance](#-how-it-works-at-a-glance)
- [Installation](#-installation)
- [Quick start](#-quick-start)
- [The student profile](#-the-student-profile)
- [Registering content](#-registering-content)
- [The priority ranking](#-the-priority-ranking)
- [Review and quiz](#-review-and-quiz)
- [File format](#-file-format)
- [Safety net](#-safety-net)
- [Architecture](#-architecture)
- [Privacy and security](#-privacy-and-security)
- [Known limitations](#-known-limitations)
- [License](#-license)

---

## 🎯 The problem

Anyone studying several subjects at once piles up three problems that are not
about content, but about organization.

**The material gets scattered.** The lecture PDF is in `Downloads`, the video
is a link lost in the browser history, the summary is in a notebook and the
exercise list is in an e-mail. When it is time to review, half of the time goes
into just gathering the pieces, and that friction is reason enough not to
review at all.

**Choosing what to review goes badly.** Left to their own devices, students
review what feels comfortable: the subject they already understand, because
reviewing it gives that nice feeling of doing well. The content they have not
mastered is exactly what they avoid, and exactly what needs reviewing.

**Forgetting gives no warning.** Retention drops silently. There is no "you
forgot Recursion" notification; you only find out during the exam.

Synapsis tackles all three. Each registered piece of content carries, in a
single file, the summary, the paths to the materials, the video lesson links
and a quiz the students wrote themselves while the subject was still fresh.
And instead of showing that list alphabetically or by registration date, the
program sorts it by a priority computed from three things: how well the student
masters that subject, how long ago they saw it, and their overall profile as a
student.

In other words: the review queue is built by the program, not by the mood of
the day.

---

## 🔭 How it works, at a glance

```
                         python synapsis.py
                                 │
                      initialize_program()  ──► creates users/ if missing
                                 │
                            show_intro()
                                 │
                              main()  ─── Main Menu ────────┐
                                 │                          │
                ┌────────────────┴────────────────┐         │
                ▼                                 ▼         │
            sign_up()                          login()      │
                │                                 │         │
     performance_coefficient()           up to 3 attempts   │
     5 weighted questions → CR                    │         │
                │                                 │         │
                └──► users/<name>/profile_<name>.txt        │
                                 │                          │
                                 └──► user_menu(name) ◄─────┘
                                            │
                                    count_access()   ──► +1 in the profile
                                            │
                                   get_study_ranking()
                                       │         │
                              delta_time()   stored difficulty
                                       └────┬────┘
                                            ▼
                               queue sorted by priority
                                            │
         ┌──────────────────────────────────┼──────────────────────────────┐
         ▼                                  ▼                              ▼
  register_content()                 review_content()               manage_studies()
         │                                  │                              │
  3 scores + quiz +              summary, attachments,          view / edit summary /
  attachments + links            links and graded quiz            rename / delete
         │
         ▼
 users/<name>/studies/<Content>.txt
```

There is no database, server or network. The program's whole state is `.txt`
files inside `users/`.

---

## 📦 Installation

**Single requirement:** Python 3.6 or newer. No external libraries: the
program only uses `os`, `sys`, `time`, `datetime` and `ast`, all from the
standard library.

```bash
git clone https://github.com/gabrieldevcode/synapsis.git
cd synapsis
python synapsis.py
```

On some Linux distributions and on macOS the command is `python3`:

```bash
python3 synapsis.py
```

The program creates the `users/` folder on its own on first run. If it cannot
(permission denied on the folder), it warns you and exits instead of carrying
on in a broken state.

### About the terminal

The interface draws frames with the `═` character (U+2550). Modern terminals
(Windows Terminal, VS Code, GNOME Terminal, iTerm2) show it without any
tweaks. On the old `cmd.exe`, if odd characters show up instead of the lines:

```bat
chcp 65001
```

---

## 🚀 Quick start

A fresh clone has no registered students, so the ranking opens empty. To see
the program with content already inside, generate a demo user:

```bash
python examples/generate_demo_user.py
```

It creates the student `demo` (password `demo123`) with four Computer Science 1
subjects registered on different dates, so the ranking has something to sort.
The data is made up.

Then just run the program, choose **1. Login** and sign in with `demo` /
`demo123`:

```
════════════════════════════════════════════════════════════
                          Hi demo
════════════════════════════════════════════════════════════
                   Registered Studies: 4
                        Accesses: 2
════════════════════════════════════════════════════════════
Priority Ranking:
PRIORITY     | CONTENT
------------------------------------------------------------
1            | Conditional Statements
2            | Loops
3            | File Handling
4            | Recursion
════════════════════════════════════════════════════════════
1. Register new content
2. Review content
3. List content (View / Edit / Delete)
4. Log out
════════════════════════════════════════════════════════════
Choice:
```

To remove the demo, just delete the folder: `rm -rf users/demo` (or
`rmdir /s users\demo` on `cmd.exe`).

---

## 📊 The student profile

At sign-up, before any content, the program runs a five-question
questionnaire, all on a scale from 1 to 10. The result is the student's
**performance coefficient (CR)**, stored in the profile and used later by the
ranking.

The weights are **not equal**, and that is a design choice, not an oversight:

| # | What the question measures | Weight |
|---|---|---|
| 1 | Keeping a routine, even without motivation | 0.10 |
| 2 | Persistence when facing complex content | 0.20 |
| 3 | Use of **active methods** (exercises, explaining out loud, summarizing) | **0.30** |
| 4 | Ability to **connect theory to practical use** | **0.30** |
| 5 | Proactivity in finding answers alone | 0.10 |

Questions 3 and 4 weigh three times as much as the first one because they are
the ones most correlated with real retention. Active study sticks better than
passive reading, and whoever can see what an abstract topic is for anchors it
to something that does not fade along with short-term memory. Consistency
matters, but consistency applied to a poor method yields little.

```
CR = p1×0.10 + p2×0.20 + p3×0.30 + p4×0.30 + p5×0.10
```

Since the weights add up to 1.0, the CR always stays on the same scale as the
answers: from 1 (low absorption) to 10 (excellent understanding).

---

## ✍️ Registering content

When registering, the program asks for a name and a summary and then three
questions from 1 to 10:

| Question | Variable | Weight |
|---|---|---|
| "If you had to teach a class on this right now, how well would you do?" | mastery | 0.5 |
| "How essential is this subject to your current goals?" | relevance | 0.3 |
| "How much do you actually enjoy learning about this?" | engagement | 0.2 |

```
difficulty = mastery×0.5 + relevance×0.3 + engagement×0.2
```

Note which way the number points: **the higher it is, the more comfortable you
are with the subject**. A high value means you could teach the class, the topic
is relevant and you enjoy it, so it needs less review. A low value is the
warning sign. The ranking uses it directly.

Then come three optional loops, each repeating while you answer `Y`:

1. **Quiz**: question and answer pairs written by you, now, while the subject
   is fresh. It is the material for future reviews.
2. **Local files**: paths to PDFs, slides, images. The program stores the
   path and never copies the file.
3. **Video lessons**: links.

Everything goes into a single `.txt` inside `users/<you>/studies/`.

---

## 🏆 The priority ranking

This is the core of the program. Every time the student area is drawn, Synapsis
reads all registered content, computes a priority for each one and sorts them.

For each piece of content, `delta_time()` turns the registration date into
elapsed hours, and then:

```
priority = CR×0.2 + difficulty×0.5 + elapsed_hours×0.5
```

The list is sorted in **ascending** order, and position 1 is the first one to
review. Since `difficulty` grows with your mastery, the content you do worst at
produces the lowest score and rises to the top of the queue, which is exactly
the desired behavior.

The CR has weight 0.2 and is the same for all of a student's content, so it
shifts every score together without ever changing their order. It exists to
calibrate the student's scale, not to reorder the queue.

### The time bands

The program also classifies the elapsed time into seven bands, each with an
associated value:

| Time since registration | Band value |
|---|---|
| less than 4 h | 10.0 |
| 4 h to 12 h | 9.2 |
| 12 h to 24 h | 8.0 |
| 24 h to 48 h | 7.0 |
| 48 h to 96 h | 5.5 |
| 96 h to 240 h | 2.0 |
| more than 240 h (10 days) | 0.5 |

The shape is that of a forgetting curve: the value drops fast in the first
hours and collapses after ten days. **These bands are computed but do not yet
feed into the score**: today the formula uses the raw number of hours. This is
described in [Known limitations](#-known-limitations), along with its practical
consequence.

---

## 🔁 Review and quiz

Option **2. Review content** opens a piece of content, shows the summary and
gathers the materials in one place:

```
              Reviewing: Conditional_Statements
════════════════════════════════════════════════════════════
Summary:
if/elif/else, comparison operators and chaining conditions. Watch out for
using = instead of == inside an if.

You can copy the relative paths below into your file explorer to open the
subject materials
Attached files:
 - materials/cs1/lecture03_conditionals.pdf
Videos related to this content:
 - https://example.invalid/lesson-conditionals
════════════════════════════════════════════════════════════
```

Then comes the quiz you wrote yourself when registering, graded question by
question:

```
                        Review Quiz
════════════════════════════════════════════════════════════
Question 1: Which operator compares equality in Python?
Answer: ==
✔ Correct!
════════════════════════════════════════════════════════════
Question 2: Is the else block required after an if?
Answer: yes
✘ Wrong. Correct answer: no
════════════════════════════════════════════════════════════
Score [████████████████████░░░░░░░░░░░░░░░░░░░░] 50.0%
You got 1 out of 2 right (50.0%).
```

The comparison ignores upper/lower case and surrounding spaces, but requires
the right text: there is no tolerance for synonyms.

---

## 📄 File format

The program's whole state is readable text. You can open, read and fix it with
any editor.

### `users/<name>/profile_<name>.txt`

Four lines, always in this order, read by index:

```
demo
demo123
6.700
2
```

| Line | Content |
|---|---|
| 1 | username |
| 2 | password (plain text, see [Known limitations](#-known-limitations)) |
| 3 | performance coefficient, 3 decimal places |
| 4 | total visits to the student area |

### `users/<name>/studies/<Content>.txt`

A four-line fixed header, followed by three named sections separated by a line
of hyphens. Each section has a variable length:

```
Content: Conditional Statements
Difficulty: 8.4
Date Added: 27/08/2026 13:51
Summary: if/elif/else, comparison operators and chaining conditions.
--------------------
QUIZ:
['Which operator compares equality in Python?', '==']
['Is the else block required after an if?', 'no']
--------------------
FILES:
materials/cs1/lecture03_conditionals.pdf
--------------------
VIDEO LESSONS:
https://example.invalid/lesson-conditionals
```

The date follows `%d/%m/%Y %H:%M` (day first). That is the format
`delta_time()` expects, and changing it by hand breaks the ranking for that
content. Each quiz line is the Python representation of a `[question, answer]`
list, read back with `ast.literal_eval` (see [Architecture](#-architecture)).

---

## 🛡️ Safety net

What the program validates and rejects, instead of accepting it and breaking
later:

| Situation | What happens |
|---|---|
| Score outside the 1 to 10 scale | Asks again until it gets a valid value |
| Text where a number is expected | Asks again, without raising an exception |
| Empty password at sign-up | Refuses and goes back to the menu |
| Username already taken | Refuses and suggests logging in |
| Login with a user that does not exist | Warns and goes back to the menu |
| Wrong password | Up to 3 attempts, then back to the menu |
| Invalid menu option | Warns and redraws the menu |
| Answer other than `Y` or `N` | Asks again |
| Picking an item outside the list | Warns and goes back |
| Deleting content | Requires typing `YES`, in capitals, in full |
| Missing or corrupted profile file | Error message, without crashing the program |
| Malformed quiz line in the `.txt` | Ignored; the review carries on |
| No permission to create `users/` | Warns and exits, instead of carrying on broken |

---

## 🏗️ Architecture

A single module, `synapsis.py`, organized in blocks by responsibility.

| Function | Role |
|---|---|
| `clear_terminal`, `line`, `header`, `typewriter`, `press_enter` | Presentation layer: everything drawn on screen goes through here |
| `initialize_program` | Makes sure `users/` exists before anything else |
| `show_intro` | Opening screen |
| `get_validated_answer` | Single entry point for every 1 to 10 score |
| `performance_coefficient` | Runs the questionnaire and returns the CR |
| `sign_up` / `login` | Create and authenticate the student |
| `count_access` | Increments and persists the total number of visits |
| `delta_time` | Turns the registration date into elapsed hours |
| `register_content` | Collects scores, quiz, attachments and links; writes the `.txt` |
| `get_study_ranking` | Reads all content and returns the sorted queue |
| `review_content` | Parses the `.txt`, shows the material and runs the quiz |
| `manage_studies` | View, edit summary, rename and delete |
| `user_menu` | Student area: brings ranking and menu together |
| `main` | Main menu and application loop |

### Design decisions

**Plain-text persistence, no database and no dependencies.** The folder is the
database: each student is a directory, each piece of content is a file. That
costs concurrency, indexing and querying: you cannot ask for "all content with
difficulty below 4" without scanning everything, which is why
`get_study_ranking` rereads the whole folder on every screen draw. In return,
the program runs on any machine with Python and nothing else, the whole state
can be inspected with a text editor, and a corrupted file takes down one piece
of content instead of the whole system. For a real student's volume (dozens of
entries, not millions) the full scan is irrelevant and readability is worth
more.

**`ast.literal_eval` instead of `eval` to read the quiz back.** The quiz is
written as the Python representation of a list and has to become a list again
when read. `eval` would do it in one line, and would also run as code whatever
was in that file. Since the format is plain text that this very README invites
you to edit, that would turn a study note into an execution vector.
`literal_eval` only accepts literals: a tampered line becomes an error, not a
command. And the error is caught, so the line is discarded and the review moves
on.

**The review parser is a per-section state machine.** The three sections
(`QUIZ:`, `FILES:`, `VIDEO LESSONS:`) have variable length, so reading by line
number would break as soon as someone added a question. `review_content` walks
the file keeping track of which section is open, and each line is interpreted
according to that context. Separator lines are skipped and lines that do not
fit are silently ignored: the file is editable by hand, so the parser is
tolerant by necessity, not by carelessness.

**Attachments are references, never copies.** The program stores the path to
the PDF or slide deck, and never copies, moves or opens the file. Students stay
in charge of organizing their own folders, Synapsis does not duplicate gigabytes
of material, and there is no code path where it could corrupt a file that is
not its own. The price is that moving the material breaks the reference, an
acceptable price compared to a study program messing with your files.

---

## 🔒 Privacy and security

The `users/` folder is in `.gitignore` and must never be versioned. It holds
the name, password and all study material of every registered person.

**Passwords are stored in plain text.** This is an academic Computer Science 1
project, and secure credential storage (salted hashing, something like `bcrypt`
or `argon2`) is outside the course scope. The practical consequence is
straightforward: **do not use a password here that you use anywhere else.**
Anyone with access to the folder can read the password by opening a `.txt`.

For the same reason, login exists to separate profiles on a shared computer:
it is not access control. There is no encryption, and deleting a user's folder
deletes everything they had.

---

## ⚠️ Known limitations

**Plain-text password.** Described in
[Privacy and security](#-privacy-and-security). It is the most serious
limitation and the only one with consequences outside the program.

**The time bands do not feed into the score.** `get_study_ranking` computes the
time band (the table in [The ranking](#-the-priority-ranking)) but uses the raw
number of hours in the formula. Since that term grows without bound, content
registered 15 days ago adds `360×0.5 = 180` points and ends up at the bottom
of the queue, when it should be at the top, which is exactly what the bands
were designed for. In practice, today the ranking prioritizes well by mastery
and poorly by time. Replacing `elapsed_hours` with the band value in the
formula is the fix.

**Renaming content does not update its internal name.** Option 3 renames the
file, but the `Content:` line inside it keeps the old name. The result is that
the listing shows the new name and the ranking keeps showing the old one.
Fixing the first line of the `.txt` solves it.

**Content names become file names.** Spaces become `_`, but characters the
operating system forbids (`\ / : * ? " < > |`) make saving fail with an error
message. Registering two pieces of content with the same name overwrites the
first one, without warning.

**The encoding is not declared.** Reading and writing use the platform default
(cp1252 on Windows, UTF-8 on most Linux systems). A `users/` folder created on
Windows and read on Linux garbles accented characters, and running with
`PYTHONUTF8=1` over old data causes a `UnicodeDecodeError`. Passing
`encoding='utf-8'` to every `open()` would solve it, at the cost of migrating
existing files.

**The score is computed but not displayed.** The screen only shows the position
in the queue, not the priority value.

**The quiz cannot be edited after it is created.** Option 3 of the menu lets
you change the summary and the name; to change a question you have to edit the
`.txt` by hand.

**There is no way to delete a user from the program.** Deleting the student's
folder is the only way.

**Data from the Portuguese version is not read.** Earlier versions stored data
in `usuarios/` with Portuguese field names. The current version only reads
`users/`; register again or regenerate the demo user.

---

## 📜 License

[MIT](LICENSE) © Gabriel Robalinho.
