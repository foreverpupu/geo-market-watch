# Contributing to Geo Market Watch

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/foreverpupu/geo-market-watch.git
cd geo-market-watch
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run schema validation tests:

```bash
pytest tests/schema_validation
```

Run pipeline tests:

```bash
python tests/pipeline/test_pipeline.py
```

---

## Contribution Types

We welcome contributions in the following areas:

- **Bug fixes** — Fix issues in existing code
- **Documentation improvements** — Clarify, expand, or correct docs
- **Benchmark cases** — Add new test cases to the benchmark suite
- **Pipeline tests** — Add regression tests for core workflows
- **Automation integrations** — Connect external data sources or tools
- **Research methodology extensions** — Improve analysis approaches

Large architectural changes should be discussed in an issue before submitting a PR.

---

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Run specific test file
   pytest tests/schema_validation/test_event_object.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Guidelines

- **Title:** Clear, concise description of changes
- **Description:** Explain what and why
- **Tests:** Include tests for new functionality
- **Documentation:** Update relevant docs
- **Breaking Changes:** Clearly mark if any

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

### Documentation

- Update README.md if adding major features
- Add to docs/ for detailed explanations
- Include examples where helpful
- Update CHANGELOG.md

---

## Development Areas

### Priority Areas

1. **Benchmark Expansion** — Add more test cases
2. **Documentation** — Improve clarity and coverage
3. **Testing** — Increase test coverage
4. **Performance** — Optimize processing speed

### Good First Issues

Look for issues labeled:
- `good first issue`
- `documentation`
- `help wanted`

---

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

---

Thank you for contributing to Geo Market Watch!
