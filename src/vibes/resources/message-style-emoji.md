# Commit Message Style Guide

## Format Structure
The commit message should follow this structure:
1. First line: <emoji> [(optional scope)] <short description>
   - Emoji: 1-3 relevant emojis (preferably 1). prefer specific emoji to a general one.
   - Scope: optional, in parentheses, only if not communicated from the emoji.
   - Description: concise summary.
2. Blank line
3. Body: detailed description.

## Description Guidelines
- Short summary of what is being done.
  What change is being made? This should summarize the major changes such that readers have a sense of what is being changed without needing to read the entire CL.
- Complete sentence, written as though it was an order.

The first line of a CL description should be a short summary of specifically what is being done by the CL, followed by a blank line.
This is what appears in version control history summaries, so it should be informative enough that future code searchers don't have to read your CL or its whole description to understand what your CL actually did or how it differs from other CLs.
That is, the first line should stand alone, allowing readers to skim through code history much faster.

Try to keep your first line short, focused, and to the point. The clarity and utility to the reader should be the top concern.

By tradition, the first line of a CL description is a complete sentence, written as though it were an order (an imperative sentence).
For example, say "Delete the FizzBuzz RPC and replace it with the new system." instead of "Deleting the FizzBuzz RPC and replacing it with the new system."
You don't have to write the rest of the description as an imperative sentence, though.

## Body Guidelines

The rest of the description should fill in the details and include any supplemental information a reader needs to understand the changelist holistically.
It might include a brief description of the problem that's being solved, and why this is the best approach.
If there are any shortcomings to the approach, they should be mentioned.
If relevant, include background information such as bug numbers, benchmark results, and links to design documents.

Why are these changes being made?
What contexts did you have as an author when making this change?
Were there decisions you made that aren't reflected in the source code? etc.

Be concise and clear. DO NOT BOAST.

## Available Commit Types and Emojis

### User-facing changes, changes that are added to changelog

#### New feature
✨ = Introduce new features.
🚩 = Add, update, or remove feature flags.
👔 = Add or update business logic.
🥚 = Add or update an easter egg.

#### Bug fix
🐛 = Fix a bug.
🚑️ = Critical hotfix.
🩹 = Simple fix for a non-critical issue.
🚨 = Fix compiler / linter warnings.

#### Improve performance
⚡️ = Improve performance.
🔍️ = Improve SEO.

#### Documentation only changes
📝 = Add or update documentation.
📄 = Add or update license.
💡 = Add or update comments in source code.
👥 = Add or update contributor(s).
✏️ = Fix typos.

#### UI/UX:
💄 = Add or update the UI and style files.
📱 = Work on responsive design.
🚸 = Improve user experience / usability.
💫 = Add or update animations and transitions.
🍱 = Add or update assets.
♿️ = Improve accessibility.
💬 = Add or update text and literals.
🌐 = Internationalization and localization.

#### Error Handling & Validation
🦺 = Add or update code related to validation.
🥅 = Catch errors.

#### Security & Authentication
🛂 = Work on code related to authorization, roles and permissions.
🔒️ = Fix security or privacy issues.


### Code changes (that the user shouldn't notice)

#### refactor: A code change that neither fixes a bug nor adds a feature
♻️ = Refactor code.
🏷️ = Add or update types.
🚚 = Move or rename resources (files, paths, routes, etc).
🔥 = Remove code or files.
🗑️ = Deprecate code that needs to be cleaned up.
⚰️ = Remove dead code.

#### style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
🎨 = Improve structure / format of the code.

#### Infrastructure & Architecture
🧵 = Add or update code related to multithreading or concurrency.
🧱 = Infrastructure related changes.
🗃️ = Perform database related changes.
👽️ = Update code due to external API changes.
💸 = Add sponsorships or money related infrastructure.
🏗️ = Make architectural changes.

#### Monitoring & Logging
🔊 = Add or update logs.
🔇 = Remove logs.
📈 = Add or update analytics or track code.
🩺 = Add or update healthcheck.


### Developer-facing changes (don't affect the user delivered parts at all)

#### test: Adding missing tests or correcting existing tests
✅ = Add, update, or pass tests.
🧪 = Add a failing test.
🤡 = Mock things.
📸 = Add or update snapshots.
🌱 = Add or update seed files.

#### build: Changes that affect the build system or external dependencies
⬇️ = Downgrade dependencies.
⬆️ = Upgrade dependencies.
📌 = Pin dependencies to specific versions.
➕ = Add a dependency.
➖ = Remove a dependency.
📦️ = Add or update compiled files or packages.

#### ci: Changes to our CI configuration files and scripts
👷 = Add or update CI build system.
💚 = Fix CI Build.

#### chore: Other changes that don't modify src or test files
🔧 = Add or update configuration files.
🔨 = Add or update development scripts.
🙈 = Add or update a .gitignore file.
🧑‍💻 = Improve developer experience.
🔐 = Add or update secrets.

#### Project Lifecycle
🎉 = Begin a project.
🔖 = Release / Version tags.
🚀 = Deploy stuff.

#### Version Control
🔀 = Merge branches.
⏪️ = Revert changes.

#### Data Analysis
⚗️ = Perform experiments.
🧐 = Data exploration/inspection.


### Additional tags (add those as needed)

#### Notices
💥 = Introduce breaking changes.

#### Code Status
🚧 = Work in progress.

#### Code Quality
🍻 = Write code drunkenly.
💩 = Write bad code that needs to be improved.
