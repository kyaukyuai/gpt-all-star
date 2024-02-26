<div align="center">
<img width="628" alt="gpt-all-star" src="https://github.com/kyaukyuai/gpt-all-star/assets/1140707/dc46fbf4-16f9-4989-801d-7df65af0c696">
<p>
AI-powered code generation tool for scratch development of web applications with a team collaboration of autonomous AI agents.
This is a research-project, and its primary value is to explore the possibility of autonomous AI agents.
</p>
</div>

<h2>Table of contents</h2>
</hr>

- [🏛 Concept](#-concept)
- [🐳 Getting Started](#-getting-started)
- [🔎 Examples](#-examples)

## 🏛 Concept

- **Build Team, Build App**: All you do is structure your team and dictate what you make.
- **AI agent collaboration**: Form a team of AI agents and collaborate with them to execute the steps.
  1. Select the appropriate a ｌeader for each step.
  2. Leaders develop an action plan for each step.
  3. Collaborate with team members to execute each task in the action plan.

![gpt-all-star-concept](https://github.com/kyaukyuai/gpt-all-star/assets/1140707/f85f05d3-2427-4af9-b48c-99c065892b2a)

## 🐳 Getting Started

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

## 🔎 Examples

examples
