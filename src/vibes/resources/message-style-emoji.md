# Commit Message Style Guide

## Format Structure
The commit message should follow this structure:
1. First line: <emoji> [(optional scope)] <short description>
   - Emoji: 1-3 relevant emojis (preferably 1)
   - Scope: optional, in parentheses
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

## Available Commit Types and Emojis
```
# API changes
## feat: A new feature
✨:sparkles:Introduce new features.
💄:lipstick:Add or update the UI and style files.
📈:chart-with-upwards-trend:Add or update analytics or track code.
🌐:globe-with-meridians:Internationalization and localization.
🍱:bento:Add or update assets.
♿️:wheelchair:Improve accessibility.
💬:speech-balloon:Add or update text and literals.
🔊:loud-sound:Add or update logs.
🔇:mute:Remove logs.
🚸:children-crossing:Improve user experience / usability.
🥚:egg:Add or update an easter egg.
💫:dizzy:Add or update animations and transitions.
🛂:passport-control:Work on code related to authorization, roles and permissions.
👔:necktie:Add or update business logic.
💸:money-with-wings:Add sponsorships or money related infrastructure.

## fix: A bug fix
🐛:bug:Fix a bug.
🚑️:ambulance:Critical hotfix.
🔒️:lock:Fix security or privacy issues.
🚨:rotating-light:Fix compiler / linter warnings.
💚:green-heart:Fix CI Build.
✏️:pencil2:Fix typos.
👽️:alien:Update code due to external API changes.
🥅:goal-net:Catch errors.
🩹:adhesive-bandage:Simple fix for a non-critical issue.

# code changes
## perf: A code change that improves performance
⚡️:zap:Improve performance.
📱:iphone:Work on responsive design.
🔍️:mag:Improve SEO.
🧵:thread:Add or update code related to multithreading or concurrency.

## refactor: A code change that neither fixes a bug nor adds a feature
🔥:fire:Remove code or files.
♻️:recycle:Refactor code.
🚚:truck:"Move or rename resources (e.g.: files, paths, routes)."
🏗️:building-construction:Make architectural changes.
🏷️:label:Add or update types.
🗑️:wastebasket:Deprecate code that needs to be cleaned up.
⚰️:coffin:Remove dead code.

## style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
🎨:art:Improve structure / format of the code.

# code adjecnt changes
## docs: Documentation only changes
📝:memo:Add or update documentation.
📄:page-facing-up:Add or update license.
💡:bulb:Add or update comments in source code.
👥:busts-in-silhouette:Add or update contributor(s).

## test: Adding missing tests or correcting existing tests
✅:white-check-mark:Add, update, or pass tests.
🤡:clown-face:Mock things.
⚗️:alembic:Perform experiments.
🌱:seedling:Add or update seed files.
🧐:monocle-face:Data exploration/inspection.
🧪:test-tube:Add a failing test.
🦺:safety-vest:Add or update code related to validation.

# non-code changes
## build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
🔐:closed-lock-with-key:Add or update secrets.
⬇️:arrow-down:Downgrade dependencies.
⬆️:arrow-up:Upgrade dependencies.
📌:pushpin:Pin dependencies to specific versions.
➕:heavy-plus-sign:Add a dependency.
➖:heavy-minus-sign:Remove a dependency.
📦️:package:Add or update compiled files or packages.
📸:camera-flash:Add or update snapshots.

## ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
👷:construction-worker:Add or update CI build system.

## chore: Other changes that don't modify src or test files
🚀:rocket:Deploy stuff.
🎉:tada:Begin a project.
🔖:bookmark:Release / Version tags.
🔧:wrench:Add or update configuration files.
🔨:hammer:Add or update development scripts.
🗃️:card-file-box:Perform database related changes.
🙈:see-no-evil:Add or update a .gitignore file.
🚩:triangular-flag-on-post:Add, update, or remove feature flags.
🩺:stethoscope:Add or update healthcheck.
🧱:bricks:Infrastructure related changes.
🧑‍💻:technologist:Improve developer experience.

# special git commits
## revert:
⏪️:rewind:Revert changes.

## merge:
🔀:twisted-rightwards-arrows:Merge branches.

# additional icons
## code-rank:
🚧:construction:Work in progress.
💩:poop:Write bad code that needs to be improved.
🍻:beers:Write code drunkenly.

## api-rank
💥:boom:Introduce breaking changes.
```
