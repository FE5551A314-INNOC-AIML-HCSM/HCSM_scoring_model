# Tests Folder

This folder contains test scripts for ensuring code quality, model performance, and data integrity across the project.

## Folder Structure
- `unit_tests/`: Tests for individual functions and modules.
- `integration_tests/`: Tests for entire pipelines or workflows.
- `model_tests/`: Validates model performance and ensures no drift over time.
- `regression_tests/`: Ensures changes don’t negatively impact existing functionality.
- `data_quality_tests/`: Tests data schemas and checks for data integrity.
- `performance_tests/`: Load and latency tests for real-time models.

## Notes
- **Automation**: Use CI/CD to automate test execution on new commits.
- **Test Coverage**: Aim for comprehensive test coverage across the project.
