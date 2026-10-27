# Instructions
1. Carefully analyze the user request received in the prompt.
2. Read the skills inside `skills/`.
3. Design a detailed, modular, and actionable technical strategy.
4. Generate the plan content and save it to a file inside the `plans/` directory (e.g., `plans/plan_feature_auth.md`).
5. Return the response using the structured schema:
   - `success`: Boolean (`true` if the plan was created and saved to disk successfully, `false` otherwise).
   - `filename`: Path or name of the saved file (e.g., `plans/plan_feature_auth.md`).