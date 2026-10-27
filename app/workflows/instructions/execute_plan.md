# Instructions
1. Locate and read the implementation plan file associated with the task.
2. Read the skills inside `skills/` to ensure full compliance with coding conventions and architectural standards.
3. Execute the implementation plan step by step:
   - Create, update, or remove files as defined in the plan.
   - Follow existing project patterns, strict type hints, and clean code practices.
4. Generate an execution summary report and save it to a file inside the `summaries/` directory (e.g., `summaries/summary_feature_auth.md`).
5. Return the response using the structured schema:
   - `success`: Boolean (`true` if all plan steps were successfully executed and verified, `false` otherwise).
   - `summary_file`: Path to the execution summary file (e.g., `summaries/summary_feature_auth.md`).

# Project Context
The backend is a Laravel project located at `/workspace/skeleton-laravel-back`. All file modifications, command executions, and tests must target this application.