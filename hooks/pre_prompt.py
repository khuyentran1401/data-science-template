from cookiecutter.main import cookiecutter
import questionary

def get_questions():
    """
    Return the set of questions that must be send to the user.
    """
    questions = questionary.form(
        project_name = questionary.text("Project name:"),
        author_name = questionary.text("Author name:"),
        dep_manager = questionary.select(
            "Select dependency manager:",
            choices=["pip", "poetry"],
            default="pip"
        ),
    )

    return questions

if __name__ == "__main__":
    questions = get_questions()
    answers = questions.ask()
    # Run Cookiecutter with the customized context
    cookiecutter(
        'https://github.com/tapyu/to-rm-data-science-template',
        no_input=True,  # Do not use cookiecutter prompt for input. Instead, use the provided context
        extra_context={"cookiecutter": answers}
    )