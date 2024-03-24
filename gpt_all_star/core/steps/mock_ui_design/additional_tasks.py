additional_tasks = [
    {
        "action": "Add a new file",
        "working_directory": ".",
        "filename": "design_000.html",
        "command": "",
        "context": """This process involves creating the actual screen design based on the specifications.
The engineer is to actually reproduce this screen layout.
Users will also be using the design UI you have generated.

Therefore, it is necessary to follow the human interface guidelines and create every detail.
""",
        "objective": """Create a screen design document.

[output format].
Outputs all of one HTML file.
The contents of this HTML file will contain the CSS and JavaScript code needed to represent the screen design, but the CSS and JavaScript files should not be loaded.
You may use a CDN, but we'd like to avoid using it as much as possible.

[important].
This HTML file is treated like a document.
It will later be given to the engineer as a screen design document.
The screen design needs to look like it was designed by a professional, not by an amateur!

This screen design should not be rendered using a drawing engine or DOM library. Please be aware that we only want to represent the screen design, so use HTML, CSS, and JS that are close to the defaults!
""",
        "reason": """If the UI is not designed for users to use, users will find it very inconvenient and complain.
Also, if the design is not clear, engineers will not be able to develop it.
Screen design needs your creativity.
""",
    },
]
