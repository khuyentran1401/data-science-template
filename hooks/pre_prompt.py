import questionary
import json

def get_questions() -> questionary.Form:
    """
    Return the set of questions that must be send to the user.
    """
    questions = questionary.form(
        project_name = questionary.text("Project name:"),
        author_name = questionary.text("Author name:"),
        compatible_python_versions = questionary.text("Pyhton version:", default="^3.8"),
        dep_manager = questionary.select(
            "Select dependency manager:",
            choices=["pip", "poetry"],
            default="pip"
        ),
    )

    return questions

def rewrite_cookiecutter_json(answers) -> None:
    """
    Rewrite
    """
    with open("cookiecutter.json", "w") as json_file:
        json.dump(answers, json_file, indent=4)

if __name__ == "__main__":
    questions = get_questions()
    answers = questions.ask()
    answers["directory_name"] = answers["project_name"].replace(' ','-').lower()
    rewrite_cookiecutter_json(answers)
