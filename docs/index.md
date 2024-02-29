<div align="center">
<img width="628" alt="gpt-all-star" src="https://github.com/kyaukyuai/gpt-all-star/assets/1140707/dc46fbf4-16f9-4989-801d-7df65af0c696">

<p>
AI-powered code generation tool for scratch development of web applications with a team collaboration of autonomous AI agents.
This is a research-project, and its primary value is to explore the possibility of autonomous AI agents.
</p>
</div>

![gpt-all-star-demo](https://github.com/kyaukyuai/gpt-all-star/assets/1140707/1ec23255-7463-4510-90fc-80b15eb64cb9)

## 🏛 Concept

- **Build Team, Build App**: Simply organize your team and decide on what to build.
- **AI Agent Collaboration**: Assemble a group of AI agents and work together to carry out the steps.
  1. Choose the right ｌeader for each step.
  2. Leaders create a plan of action for each step.
  3. Work with team members to complete every task in the action plan.

![gpt-all-star-concept](https://github.com/kyaukyuai/gpt-all-star/assets/1140707/77bdd5fa-afe9-4e3c-8dfd-85399852aec6)

## 🐳 Getting Started

### For User

1. Installation

```bash
$ pip install gpt-all-star
```

2. Set the `GPT ALL STAR` environment variables

```bash
$ export OPENAI_API_MODEL_NAME=gpt-4-turbo-preview
$ export OPENAI_API_KEY=<your-openai-api-key>
```

3. Fun `GPT ALL STAR`

```bash
$ gpt-all-star
```

### For Developer

:bulb: While it's entirely feasible to launch the application on your local machine directly, we **strongly recommend** using **Docker** for starting up the application.

1. Clone the repository

```bash
$ git clone git@github.com:kyaukyuai/gpt-all-star.git
```

2. Edit the `.env` file

```bash
$ mv .env.sample .env
```

3. Run `docker compose build` and `docker compose up`

```bash
$ make build
$ make up
```

4. Open the web terminal `port 7681`

Open: http://localhost:7681

5. Install dependencies

```bash
$ poetry install
```

6. Start `GPT ALL STAR`

```bash
$ poetry run gpt-all-star
```

7. Edit the team members

If you want to change the team members, edit the `gpt_all_star/agents.yml` file.

## 🕴 Current Situation

This is a research project and the main focus is currently on validating `Client Web Applications` in `React` and `ChakraUI` using `JavaScript`.
We would like to test other languages and libraries as well and welcome contributions.

## 🔎 Examples

### ⏱️ Pomodoro Timer

- 💬 Instruction: `Pomodoro Timer fully designed by human interface guideline`
- 💻️ [GitHub](https://github.com/gpt-all-star/pomodoro)

![Export-1707059574807](https://github.com/kyaukyuai/gpt-all-star/assets/1140707/c194dced-d179-4d1e-8e5d-f89dbafa00ee)
