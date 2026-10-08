import os
import sys
import time
import datetime
import ast



# LAYOUT AND DESIGN
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def line():
    print("═" * 60)


def header(text):
    clear_terminal()
    line()
    print(text.center(60))
    line()


def typewriter(text, delay=0.02):
    if not animations_enabled():
        print(text)
        return
    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()


def press_enter():
    input("\nPress ENTER to continue...")






# ANIMATIONS
#
# Every animation draws its frames on a single line with '\r' and always ends
# by printing the final frame, so the screen looks the same with or without
# the motion. Set SYNAPSIS_NO_ANIMATION=1 to skip the motion entirely (slow
# terminals, screen readers, or just to go faster) and NO_COLOR=1 to drop the
# colors.

SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
FRAME_TIME = 0.08 # seconds each frame stays on screen

CYAN, GREEN, RED, GRAY = 45, 42, 203, 244 # 256-color palette codes


def animations_enabled():
    return os.environ.get('SYNAPSIS_NO_ANIMATION', '') == ''


def colors_enabled():
    return os.environ.get('NO_COLOR', '') == '' and sys.stdout.isatty()


# On Windows, running any shell command switches the console into the mode
# that understands ANSI escape codes (colors and cursor movement)
def enable_ansi():
    if os.name == 'nt':
        os.system('')


def paint(text, color):
    if not colors_enabled():
        return text
    return f"\033[38;5;{color}m{text}\033[0m"


def pause(seconds):
    if animations_enabled():
        time.sleep(seconds)


# Spins next to a message for a moment, then swaps the spinner for a check
# mark, or for a cross when the step failed (ok=False)
def spinner(message, duration=1.0, ok=True):
    if animations_enabled():
        for i in range(int(duration / FRAME_TIME)):
            frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
            print(f"\r{paint(frame, CYAN)} {message}", end="", flush=True)
            time.sleep(FRAME_TIME)
    result = paint('✔', GREEN) if ok else paint('✘', RED)
    print(f"\r{result} {message}")


# Draws a bar like ███████░░░ for a fraction between 0 and 1
def bar(fraction, width=30):
    fraction = min(max(fraction, 0), 1)
    filled = round(fraction * width)
    return paint("█" * filled, CYAN) + paint("░" * (width - filled), GRAY)


def progress_bar(label, duration=1.5, width=30):
    steps = 30 if animations_enabled() else 0
    for step in range(steps):
        fraction = step / steps
        print(f"\r{label} [{bar(fraction, width)}] {fraction:4.0%}", end="", flush=True)
        time.sleep(duration / steps)
    print(f"\r{label} [{bar(1, width)}] 100%")


# Fills a bar while the number counts up from zero to the final value
def animated_meter(label, value, maximum=10, decimals=2, duration=1.2, width=30, suffix=""):
    steps = 40 if animations_enabled() else 0
    for step in range(steps):
        current = value * step / steps
        print(f"\r{label} [{bar(current / maximum, width)}] {current:.{decimals}f}{suffix}", end="", flush=True)
        time.sleep(duration / steps)
    print(f"\r{label} [{bar(value / maximum, width)}] {value:.{decimals}f}{suffix}")


# Prints one line at a time, like a list sliding onto the screen
def reveal_lines(lines, delay=0.06):
    for text in lines:
        print(text)
        pause(delay)


LOGO = [
    '█████ █   █ █   █  ███  ████  █████ █████ █████',
    '█      █ █  ██  █ █   █ █   █ █       █   █    ',
    '█████   █   █ █ █ █████ ████  █████   █   █████',
    '    █   █   █  ██ █   █ █         █   █       █',
    '█████   █   █   █ █   █ █     █████ █████ █████',
]
LOGO_GRADIENT = [51, 45, 39, 33, 27] # one shade of blue per logo row


# A signal fires along an axon and lights up each neuron it reaches: ●━━━━●────○
def synapse_pulse(width=41):
    neurons = (0, width // 2, width - 1)

    def frame(signal):
        cells = []
        for i in range(width):
            if i in neurons:
                cells.append(paint('●', GREEN) if i <= signal else paint('○', GRAY))
            elif i == signal:
                cells.append(paint('◆', CYAN))
            else:
                cells.append(paint('━', CYAN) if i < signal else paint('─', GRAY))
        return ' ' * ((60 - width) // 2) + ''.join(cells)

    if animations_enabled():
        for signal in range(width):
            print(f"\r{frame(signal)}", end="", flush=True)
            time.sleep(0.025)
    print(f"\r{frame(width)}")


def show_logo():
    clear_terminal()
    print()
    for row, color in zip(LOGO, LOGO_GRADIENT):
        print(paint(row.center(60), color))
        pause(0.08)
    print()
    synapse_pulse()


def say_goodbye():
    clear_terminal()
    print()
    line()
    typewriter("Thank you for using Synapsis.".center(60), 0.03)
    typewriter("See you soon!".center(60), 0.03)
    line()
    print()
    synapse_pulse()
    print()





# INTRODUCTION

# Creates the users folder when the program starts
def initialize_program():

    users_folder = 'users'

    if not os.path.exists(users_folder): # Checks whether it exists, creates it if not
        try:
            os.makedirs(users_folder) # create
        except OSError as e: # the machine may be blocking it
            print(f"Critical error while creating directory '{users_folder}': {e}")
            print("Please check the folder permissions and try again.")
            exit()





# Short explanation of the application
def show_intro():

    show_logo()
    print()
    line()
    print("Welcome to SYNAPSIS".center(60))
    line()

    msg = ("""
    Our mission is to turn reviewing what you study
    into an intuitive, effective and smart routine.

    Synapsis uses spaced repetition to automatically
    schedule your reviews at the right moment.

    Let's beat disorganization together.
    """)
    
    typewriter(msg)
    line()
    press_enter()






# validates the answers of the questionnaires that follow
def get_validated_answer(question):
    while True:
        try:
            print(question)
            answer = float(input('→ '))
            if 1 <= answer <= 10: # sets the limits
                return answer
            else:
                print('Enter a value between 1 and 10\n')

        except:
            print("Invalid input, type only numbers from 1 to 10\n")






# Defines the user's quality as a student
def performance_coefficient():

    header("Finding Your Pace")
    print()


    typewriter("The following questions are meant to personalize your \n" \
    "experience in Synapsis " \
    "and improve how you study  \n" \
    "with spaced repetition", 0.01)

    print()
    time.sleep(0.5)

    typewriter("The questions are personal and are not meant to embarrass you,\n" \
    "but to help your own growth!", 0.01)

    print()
    time.sleep(0.5)
    line()

    print('''
Answer every question on a scale from 1 to 10, where:

1: I don't relate to this at all / I'm very weak at this.

10: I relate to this completely / I'm excellent at this.

''')
    line()
    press_enter()
    clear_terminal()




    print(
        '''
1: I don't relate to this at all / I'm very weak at this.

10: I relate to this completely / I'm excellent at this.
'''
    )
    print()

# QUESTIONS


    p1 = get_validated_answer("On a scale from 1 to 10, how well can you keep a daily study routine, \neven on the days when you feel no motivation at all to study?")
    p2 = get_validated_answer("From 1 to 10, how persistent are you when you face complex content \nthat you don't understand on the first try?")
    p3 = get_validated_answer("From 1 to 10, how much do you use active study methods (such as solving exercises, \nexplaining the subject out loud or writing your own summaries) instead of just \nconsuming passively (only reading or watching video lessons)?")
    p4 = get_validated_answer("When studying a boring theoretical topic, from 1 to 10, how well can you picture \nhow it will help you solve real problems in your future career?")
    p5 = get_validated_answer("From 1 to 10, if the course material is poor or incomplete, how proactive are you in \nfinding the answer on your own in documentation, books or AI, without relying on a teacher?")

# ==============================================================================================================


    clear_terminal()
    header('Questionnaire Completed Successfully!!!')



# PERFORMANCE COEFFICIENT EQUATION


    weight1, weight2, weight3, weight4, weight5 = 0.1, 0.2, 0.3, 0.3 , 0.1
    quality = p1 * weight1 + p2 * weight2 + p3 * weight3 + p4 * weight4 + p5 * weight5

    print()
    progress_bar("Analyzing your answers ", duration=1.5, width=25)
    print()
    typewriter("Your performance coefficient is:")
    animated_meter("CR", quality, maximum=10, width=40)
    print('\n1 → low content absorption \n' \
    '10 → excellent understanding of the subjects')
    press_enter()

#==============================================================================================================

    return quality







# LOGIN AND SIGN-UP FUNCTIONS


def sign_up():
    users_folder = 'users' # created when the application starts
    header("User Sign-up")
    print()

    name = input("Username: ")
    print()
    password = input("Create a password: ")
    if password == '': # simple password check
        print(f"\n Your password cannot be empty")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return

    print()
    line()

    user_path = os.path.join(users_folder, name) # path to this specific user's folder

    if os.path.exists(user_path): # checks, through the folder names, whether someone already has this username
        print("\nError: This username already exists.")
        print("Try a different name or log in.\n")
        line()
        input('Press ENTER to go back to the menu')
        return

    print()
    typewriter('Now we will set up your student profile')
    press_enter()

    questionnaire_result = performance_coefficient()

    clear_terminal()
    print()
    spinner("Creating your profile", 1.2)

    try:
        os.makedirs(user_path)
        profile_file_path = os.path.join(user_path, f'profile_{name}.txt') # sign-up information saved in a txt file

        with open(profile_file_path, "w") as f:
            f.write(f'{name}\n')
            f.write(f'{password}\n')
            f.write(f'{questionnaire_result:.3f}\n')
            f.write('0\n') # total logins made

        clear_terminal()
        header("Sign-up completed successfully!")
        time.sleep(4)

    except OSError as e:
        print(f"\nError while creating the folder or file: {e}")
        print("Please try again.")
        time.sleep(3)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        time.sleep(3)



def login():

    users_folder = 'users'
    header("Login")
    print()
    print("Name")
    name = input("→ ")

    #personal_info
    user_path = os.path.join(users_folder, name)
    profile_path = os.path.join(user_path, f'profile_{name}.txt')

    # checks whether the name matches any folder
    if not os.path.exists(user_path):
        typewriter("\nUser not found.", 0.03)
        typewriter("Check the username or sign up.", 0.03)
        time.sleep(1)
        input('Press ENTER to go back to the menu')
        return


    # Reads the correct password from the profile file
    correct_password = None
    try:
        with open(profile_path, 'r') as f:
            lines = f.readlines()
        correct_password = lines[1].strip() # the password is on line 2, so index 1


    except FileNotFoundError:
        print(f"\n File '{profile_path}' was not found.")
        print("Something went wrong during sign-up.")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return

    except Exception as e:
        print(f"\n An error occurred while reading the profile: {e}")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return


    # Password attempts
    max_attempts = 3
    # Limits how many times the password can be tried
    for current_attempt in range(1, max_attempts + 1):
        print()
        if current_attempt == 1:
            print("Password")
        else:
            print(f"(Attempt {current_attempt} of {max_attempts})")
            print('Password:')

        typed_password = input("→ ")
        password_ok = typed_password == correct_password

        print()
        spinner("Checking your password", 0.6, ok=password_ok)

        if password_ok:
            typewriter('\nLogin successful! Taking you to your study area...', 0.03)
            time.sleep(2)
            return name
        else:
            typewriter(f"\nYour password is incorrect. Try again:")

    print("\n[ERROR] Maximum number of attempts exceeded.")
    time.sleep(2)
    return










#   USER AREA


## HELPER FUNCTIONS

# Counts how many times the user has opened the application, to provide a better experience
def count_access(username):

    user_path = os.path.join('users', username, f'profile_{username}.txt')
    access_count_index = 3 # line of the user's profile file that holds the number of accesses

    try:
        try:
            with open(user_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print('Error finding the profile file')
            return


        current_accesses = int(lines[access_count_index].strip()) # converts from str to int

        new_access = current_accesses + 1 # adds 1 to the access count

        lines[access_count_index] = f'{new_access}\n' # updates the list

        with open(user_path, 'w') as f: # rewrites the profile file, now with +1 access
            f.writelines(lines)

        return new_access # returns the current number of accesses

    except Exception as e:
        print(f"Unexpected error while processing accesses for '{username}': {e}")
        return 1



# computes the difference between now and the moment the user registered the content
def delta_time(date, hour):

    start_datetime = datetime.datetime.strptime(f"{date} {hour}", "%d/%m/%Y %H:%M") # parses the time

    now = datetime.datetime.now()
    difference = now - start_datetime
    elapsed_hours = difference.total_seconds() / 3600.0

    return elapsed_hours # returns the total time














## THE FUNCTIONS THAT MAKE THE APPLICATION STAND OUT

# saves the desired content in an organized way
def register_content(username):
    header("New Study Entry")

    # repository for the studies
    studies_folder = os.path.join('users', username, 'studies')

    if not os.path.exists(studies_folder): # create it if missing
        os.makedirs(studies_folder)

    # content info
    content_name = input("Content/Subject name: ")
    reference_text = input("Description or summary of the content: ")

    # questionnaire to assess how well the user understands it
    print("\nAnswer everything on a scale from 1 to 10:")
    mastery = get_validated_answer("If you had to teach a class on this right now, how well would you do?")
    relevance = get_validated_answer("How essential is this subject to your current goals?")
    engagement = get_validated_answer("How much do you actually enjoy learning about this?")

    difficulty = ((mastery*0.5) + (relevance*0.3) + (engagement*0.2)) # assigned difficulty

    registration_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")



    # --- Register Quiz ---
    quiz_data = []
    print("\n--- Quick Quiz for future reviews ---")
    while True:
        option = input("Do you want to add a question to the quiz? (Y/N): ").upper()
        if option == 'Y':
            question = input("Question: ")
            answer = input("Correct answer: ")
            quiz_data.append([question, answer])
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")

    # --- Local Files ---
    file_paths = []
    print("\n--- Attach Files from Your Computer ---")
    print('-> Add the relative paths of: slides, documents, images, etc..')
    while True:
        option = input("Do you want to save the path of a local file? (Y/N): ").upper()
        if option == 'Y':
            path = input("Paste the file path here: ").strip('"')
            file_paths.append(path)
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")

    # --- Video Lessons ---
    links = []
    print("\n--- Save Video Lesson Links ---")
    while True:
        option = input("Do you want to save a video lesson link? (Y/N): ").upper()
        if option == 'Y':
            link = input("Paste the video link here: ")
            links.append(link)
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")


    # --- Saving the File ---
    file_name = f"{content_name.replace(' ', '_')}.txt"
    final_path = os.path.join(studies_folder, file_name)


    print()
    spinner("Saving your content", 0.8)

    # Saves the study info in the txt file
    try:
        with open(final_path, 'w') as f:

            f.write(f"Content: {content_name}\n")
            f.write(f"Difficulty: {difficulty}\n")
            f.write(f"Date Added: {registration_time}\n")
            f.write(f"Summary: {reference_text}\n")
            f.write("-" * 20 + "\n")
            f.write("QUIZ:\n")
            for item in quiz_data:
                f.write(f"{item}\n")
            f.write("-" * 20 + "\n")
            f.write("FILES:\n")
            for file in file_paths:
                f.write(f"{file}\n")
            f.write("-" * 20 + "\n")
            f.write('VIDEO LESSONS:\n')
            for video in links:
                f.write(f'{video}\n')


        line()
        typewriter("Content saved successfully!", 0.02)
        line()
        time.sleep(1)

    except Exception as e:
        print(f"Error while saving: {e}")
        press_enter()








# Uses the computed-priority algorithm to build the sorted list of reviews
def get_study_ranking(username, student_quality):

    studies_folder = os.path.join('users', username, 'studies')
    # Fetches all of the user's studies
    try:
        files = []
        full_list = os.listdir(studies_folder)

        for file in full_list:
            files.append(file)

    except Exception:
        return []


    # Extracting data from each study file
    ranked_list = []
    for study in files:
        study_full_path = os.path.join(studies_folder, study)

        with open(study_full_path, 'r') as f:
            data = f.readlines()
            content_name = data[0].strip().replace("Content: ", "")
            user_assigned_difficulty = float(data[1].strip().replace("Difficulty: ", ""))

            date_added = data[2].strip().replace('Date Added: ', '')
            day_hour = date_added.split(' ')
            day = day_hour[0]
            hour = day_hour[1]

            elapsed_time = delta_time(day, hour) # time difference function

            # For a better priority calculation, I defined a few time bands to tell whether little, some or a lot of time has passed
            if elapsed_time < 4:
                tv = 10.0
            elif 4 <= elapsed_time < 12:
                tv = 9.2
            elif 12 <= elapsed_time < 24:
                tv = 8.0
            elif 24 <= elapsed_time < 48:
                tv = 7.0
            elif 48 <= elapsed_time < 96:
                tv = 5.5
            elif 96 <= elapsed_time < 240:
                tv = 2.0
            else:
                tv = 0.5


            # The higher the result, the lower the need to review the content
            computed_priority = student_quality* 0.2 + user_assigned_difficulty * 0.5 + elapsed_time *0.5

            # Adds it to the list
            ranked_list.append([computed_priority, content_name])


    ranked_list.sort(key=lambda x: x[0])

    return ranked_list









# an effective way to review what you have already registered
def review_content(username):

    studies_folder = os.path.join('users', username, 'studies')
    if not os.path.exists(studies_folder):
        print("No studies registered yet.")
        time.sleep(1)
        return

    files = []


    full_list = os.listdir(studies_folder)

    for file in full_list:
        if file.endswith('.txt'):
            files.append(file)

    if not files:
        print("No studies registered yet.")
        time.sleep(1)
        return

    header("Review Content")
    print("Choose the content to review:")

    for i, file in enumerate(files): # best way to walk a list while knowing its index
        print(f"{i+1}. {file.replace('.txt','').replace('_',' ')}")

    print()
    print("Type 0 to go back")

    # validating the value
    try:
        line()
        choice = int(input("Option: "))
        line()
    except ValueError:
        print("Invalid input.")
        time.sleep(1)
        return
    if choice == 0:
        return
    if choice < 1 or choice > len(files):
        print("Invalid option.")
        time.sleep(1)
        return

    # keeps track of the chosen file
    chosen_file = files[choice-1]
    path = os.path.join(studies_folder, chosen_file)
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error opening the file: {e}")
        time.sleep(1)
        return

    # shows the summary
    summary = ""
    quiz = []
    local_files = []
    videos = []
    reading_quiz = False
    reading_files = False
    reading_videos = False


    for ln in lines:
        # skip separator lines
        if ln.strip().startswith("-"):
            continue

        if ln.startswith("Summary:"):
            summary = ln.replace("Summary:", "").strip()
            reading_quiz = reading_files = reading_videos = False

        elif ln.strip() == "QUIZ:":
            reading_quiz = True
            reading_files = reading_videos = False
            continue

        elif ln.strip() == "FILES:":
            reading_files = True
            reading_quiz = reading_videos = False
            continue

        elif ln.strip() == "VIDEO LESSONS:":
            reading_quiz = reading_files = False
            reading_videos = True
            continue

        if reading_quiz and ln:
            try:
                # Turns the string "['Q', 'A']" into a real list ['Q', 'A']
                line_data = ast.literal_eval(ln)
                if isinstance(line_data, list):
                    quiz.append(line_data)
            except:
                # If the line is not a valid list, ignore it
                continue
        elif reading_files:
            local_files.append(ln.strip())
        elif reading_videos:
            videos.append(ln.strip())

    header(f"Reviewing: {chosen_file.replace('.txt','')}")
    print("Summary:")
    print(summary)
    print()
    if local_files:
        print('You can copy the relative paths below into your file explorer to open the subject materials')
        print("Attached files:")
        for file in local_files:
            print(f" - {file}")
    if videos:
        print("Videos related to this content:")
        for v in videos:
            print(f" - {v}")
    line()
    press_enter()


    # Take the quiz if there is one
    if not quiz:
        print("No quiz registered for this content.")
        press_enter()
        return

    header("Review Quiz")
    correct_answers = 0
    for i, (question, correct_answer) in enumerate(quiz, start=1):
        print(f"Question {i}: {question}")
        user_answer = input("Answer: ").strip()
        if user_answer.lower() == str(correct_answer).strip().lower():
            print(paint("✔ Correct!", GREEN))
            correct_answers += 1
        else:
            print(paint("✘ Wrong.", RED) + f" Correct answer: {correct_answer}")
        line()
        time.sleep(0.8)

    total = len(quiz)
    percentage = (correct_answers/total)*100
    animated_meter("Score", percentage, maximum=100, decimals=1, width=40, suffix="%")
    print(f"You got {correct_answers} out of {total} right ({percentage:.1f}%).")
    press_enter()




def manage_studies(username):

    studies_folder = os.path.join('users', username, 'studies')
    if not os.path.exists(studies_folder):
        print("No studies registered yet.")
        time.sleep(1)
        return

    while True:
        header("Your Studies - List / Edit / Delete")
        files = []
        all_items = os.listdir(studies_folder)
        for item in all_items:
            files.append(item)


        if not files:
            print("No studies registered yet.")
            press_enter()
            return

        for i, file in enumerate(files):
            print(f"{i+1}. {file.replace('.txt','').replace('_',' ')}")
        print("0. Back")
        try:
            choice = int(input("Pick an item to view/edit/delete (number): "))
        except ValueError:
            print("Invalid input.")
            time.sleep(1)
            continue

        if choice == 0:
            return
        if choice < 1 or choice > len(files):
            print("Invalid option.")
            time.sleep(1)
            continue

        selected_file = files[choice-1]
        path = os.path.join(studies_folder, selected_file)
        # show options
        header(f"Content: {selected_file.replace('.txt','')}")
        print("1. View content")
        print("2. Edit summary")
        print("3. Rename content")
        print("4. Delete content")
        print("0. Back")
        op = input("Option: ")

        if op == '1':
            try:
                with open(path, 'r') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error opening the file: {e}")
            press_enter()

        elif op == '2':
            # edit summary (the line that starts with 'Summary:')
            try:
                with open(path, 'r') as f:
                    lines = f.readlines()
                for idx, l in enumerate(lines):
                    if l.startswith("Summary:"):
                        print("Current summary:")
                        print(l.replace("Summary:", "").strip())
                        new = input("New summary (leave empty to keep it): ")
                        if new.strip() != "":
                            lines[idx] = f"Summary: {new}\n"
                        break
                with open(path, 'w') as f:
                    f.writelines(lines)
                print("Summary updated successfully.")
            except Exception as e:
                print(f"Error while editing: {e}")
            press_enter()

        elif op == '3':
            new_name = input("Type the new content name (name only, no extension): ").strip()
            if new_name == "":
                print("Invalid name.")
                time.sleep(1)
            else:
                new_file = f"{new_name.replace(' ', '_')}.txt"
                new_path = os.path.join(studies_folder, new_file)
                try:
                    os.rename(path, new_path)
                    print("Renamed successfully.")
                except Exception as e:
                    print(f"Error while renaming: {e}")
                time.sleep(1)

        elif op == '4':
            confirmation = input(f"Are you sure you want to delete '{selected_file}'? (TYPE 'YES'): ")
            if confirmation == 'YES':
                try:
                    os.remove(path)
                    print("Content deleted successfully.")
                except Exception as e:
                    print(f"Error while deleting: {e}")
            else:
                print("Operation cancelled.")
            time.sleep(1)

        elif op == '0':
            continue
        else:
            print("Invalid option.")
            time.sleep(1)





# BRINGING THE HELPER FUNCTIONS TOGETHER INTO THE USER MENU


def user_menu(username):


    studies_folder = os.path.join('users', username, 'studies')
    if not os.path.exists(studies_folder):
        os.makedirs(studies_folder)


    profile_path = os.path.join('users', username, f'profile_{username}.txt')
    with open(profile_path, 'r') as f:
        profile_data = f.readlines()
        student_quality = float(profile_data[2].strip())


    access_count = count_access(username)

    clear_terminal()
    print()
    spinner("Loading your study area", 1.0)
    print()
    line()
    if access_count == 1:
        typewriter(f"Hi {username}! A very warm welcome to your study area!", 0.03)
        typewriter("I've got everything ready for your first visit.", 0.03)


    else:
        typewriter(f"Welcome back, {username}!", 0.03)
        print(f"Total accesses: {access_count}")
    line()
    time.sleep(1)




    first_render = True # the ranking only slides in on the first screen after login

    while True:

        all_files = os.listdir(studies_folder)
        study_count = 0
        for file in all_files:
            if file.endswith('.txt'):
                study_count = study_count + 1


        ranking = get_study_ranking(username, student_quality)

        header(f"Hi {username}")
        print(f"Registered Studies: {study_count}".center(60))
        print(f"Accesses: {access_count}".center(60))
        line()
        print("Priority Ranking:")
        if ranking:
            print(f"{'PRIORITY':<12} | {'CONTENT':<30}")
            print("-" * 60)
            rows = []
            for i, item in enumerate(ranking):
                # Reads the elements inside 'item'
                score = item[0]
                name = item[1]
                rows.append(f"{i +1: <12} | {name:<30}")
            reveal_lines(rows, delay=0.08 if first_render else 0)
            first_render = False





        else:
            print("Nothing to rank yet.")

        line()

        # Menu
        print("1. Register new content")
        print("2. Review content")
        print("3. List content (View / Edit / Delete)")
        print("4. Log out")
        line()

        choice = input("Choice: ")

        if choice == '1':
            register_content(username)

        elif choice == '2':
            review_content(username)

        elif choice == '3':
            manage_studies(username)

        elif choice == '4':
            return

        else:
            print("Invalid option. Try again.")
            time.sleep(1)






def main():

    enable_ansi()
    initialize_program()
    show_intro()
    enabled = ''
    while enabled != True:
        header("Main Menu")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")
        line()

        choice = input("Choose an option: ")

        if choice == "1":
            logged_user = login()

            if logged_user:
                user_menu(logged_user)

        elif choice == "2":
            sign_up()
        elif choice == "3":
            say_goodbye()
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)




if __name__ == "__main__":
    main()
