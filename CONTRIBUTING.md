# Contributing to Inequality App

Thank you for considering contributing to the Inequality App! This document outlines the process for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the [Issues](https://github.com/your-org/inequality-app/issues)
- If not, create a new issue with a descriptive title and clear description
- Include steps to reproduce, expected behavior, and actual behavior
- Add screenshots if applicable
- Include your environment details (OS, browser, etc.)

### Suggesting Features

- Check if the feature has already been suggested in the [Issues](https://github.com/your-org/inequality-app/issues)
- If not, create a new issue with the label "enhancement"
- Clearly describe the feature and its value to the project
- If possible, outline a technical approach to implementing it

### Pull Requests

1. Fork the repository
2. Create a new branch for your work with a descriptive name (e.g., `fix-login-page`, `add-sorting-feature`)
3. Make your changes, following the coding standards outlined below
4. Write or update tests as needed
5. Ensure all tests pass by running `make test`
6. Commit your changes using Conventional Commits (see below)
7. Push to your fork and submit a pull request to the `main` branch
8. Address any feedback in the code review

## Development Environment

To set up your development environment:

```bash
git clone https://github.com/your-org/inequality-app.git
cd inequality-app
cp .env.example .env          # add your secrets
make dev                      # boots full stack (db, api, web, airflow)
```

## Coding Standards

### General Guidelines

- Follow the existing code style and structure
- Keep functions and methods small and focused
- Write self-documenting code with clear variable and function names
- Add comments for complex logic

### Python

- Follow PEP 8 style guide
- Use Black for code formatting with 120-character line length
- Use Ruff for linting
- Always include type hints and docstrings in the Google format
- Use async/await for I/O-bound code
- Write unit tests using pytest

### TypeScript/React

- Follow Airbnb's JavaScript Style Guide
- Use functional components and hooks (no class components)
- Follow React best practices for performance
- Use the correct React component lifecycle methods
- Write tests using React Testing Library

### SQL

- Use clear and meaningful table and column names
- Write comments for complex queries
- Keep SQL queries optimized for performance

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.; no code change)
- `refactor`: Code refactoring (no feature or bug fix)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process, tooling changes, etc.

Examples:
- `feat(api): add endpoint for financial interests`
- `fix(web): resolve authentication issue on mobile devices`
- `docs: update installation instructions`

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 