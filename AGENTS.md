# AGENTS.md

## Collaboration Summary
This project was developed in collaboration with Gemini CLI, an AI-powered terminal agent. The AI assisted in the entire lifecycle of the project, from identifying missing requirements to implementing the core game engine and setting up the automated testing infrastructure.

## How AI was used
- **Core Logic Implementation**: Gemini CLI generated the entire `poker.py` game engine. This included the `HandEvaluator` for Texas Hold 'em hand rankings (including complex cases like the "Wheel" straight), the `Game` state management for betting rounds, and the CLI interface.
- **Test Design**: The AI proposed and implemented a `pytest` suite in `tests/test_poker.py` covering 6 critical areas of the application: deck management, hand ranking (Pair, Flush), betting logic, all-in handling, and AI action consistency.
- **Bug Fixing during Development**: When running the initial test suite, the AI identified an `AssertionError` where a "Pair" test case actually contained a "Straight". The AI diagnosed the overlap and surgically updated the test data to ensure correct validation.
- **CI/CD Configuration**: The AI created the GitHub Actions workflow to ensure that the project remains stable and all requirements are met on every push.
- **Project Structure**: Gemini CLI mapped the project requirements from the `README.md` and ensured all deliverables (tests, CI/CD, documentation) were present.

## Lessons Learned
- **AI as a Proactive Partner**: The AI was able to recognize that the README promised a product that didn't yet exist in the file system and proactively offered to build it.
- **Testing is Vital for AI Code**: Even with high-quality generation, edge cases (like the accidental straight in the pair test) can occur. Using the AI to both write and debug tests locally saved significant time.
- **Context Awareness**: The AI maintained context of the project instructions throughout the session, ensuring that specific requirements like "minimum 5 tests" and "GitHub Actions workflow" were strictly adhered to.
