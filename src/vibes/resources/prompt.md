I need help writing a commit message for the following changes.
Please analyze the provided information and generate a clear, concise commit message.

# Requirements
## Instructions
1. Analyze the git diff to understand the nature and scope of changes
2. Consider the project context from README.md and git ls-files
3. Consider the previous message or the provided description.
4. Choose the most appropriate commit type based on the changes, but DO NOT add a textual 'type' in the header.
5. Select 1-3 relevant emojis (prefer using 1 unless multiple aspects need emphasis)
6. Check if the commit is relevant only to a specific scope.
7. Write a message according to the format and requirements above.

Please generate a commit message that:
- Is clear and descriptive
- Uses appropriate emoji(s)
- Captures the essence of the changes
- Stays under 72 characters for the first line

## Commit Message Format
The commit message should follow this structure:
1. First line: <emoji> [(optional scope)] <short description>
   - Emoji: 1-3 relevant emojis (preferably 1)
   - Scope: optional, in parentheses
   - Description: concise summary.
2. Blank line
3. Body: detailed description.

### Description
- Short summary of what is being done.
  What change is being made? This should summarize the major changes such that readers have a sense of what is being changed without needing to read the entire CL.
- Complete sentence, written as though it was an order.

The first line of a CL description should be a short summary of specifically what is being done by the CL, followed by a blank line.
This is what appears in version control history summaries, so it should be informative enough that future code searchers don’t have to read your CL or its whole description to understand what your CL actually did or how it differs from other CLs.
That is, the first line should stand alone, allowing readers to skim through code history much faster.

Try to keep your first line short, focused, and to the point. The clarity and utility to the reader should be the top concern.

By tradition, the first line of a CL description is a complete sentence, written as though it were an order (an imperative sentence).
For example, say "Delete the FizzBuzz RPC and replace it with the new system.” instead of "Deleting the FizzBuzz RPC and replacing it with the new system.”
You don’t have to write the rest of the description as an imperative sentence, though.

### Body

The rest of the description should fill in the details and include any supplemental information a reader needs to understand the changelist holistically.
It might include a brief description of the problem that’s being solved, and why this is the best approach.
If there are any shortcomings to the approach, they should be mentioned.
If relevant, include background information such as bug numbers, benchmark results, and links to design documents.

Why are these changes being made?
What contexts did you have as an author when making this change?
Were there decisions you made that aren’t reflected in the source code? etc.

### Available Commit Types and Emojis
```
🎨:art:Improve structure / format of the code.
⚡️:zap:Improve performance.
🔥:fire:Remove code or files.
🐛:bug:Fix a bug.
🚑️:ambulance:Critical hotfix.
✨:sparkles:Introduce new features.
📝:memo:Add or update documentation.
🚀:rocket:Deploy stuff.
💄:lipstick:Add or update the UI and style files.
🎉:tada:Begin a project.
✅:white-check-mark:Add, update, or pass tests.
🔒️:lock:Fix security or privacy issues.
🔐:closed-lock-with-key:Add or update secrets.
🔖:bookmark:Release / Version tags.
🚨:rotating-light:Fix compiler / linter warnings.
🚧:construction:Work in progress.
💚:green-heart:Fix CI Build.
⬇️:arrow-down:Downgrade dependencies.
⬆️:arrow-up:Upgrade dependencies.
📌:pushpin:Pin dependencies to specific versions.
👷:construction-worker:Add or update CI build system.
📈:chart-with-upwards-trend:Add or update analytics or track code.
♻️:recycle:Refactor code.
➕:heavy-plus-sign:Add a dependency.
➖:heavy-minus-sign:Remove a dependency.
🔧:wrench:Add or update configuration files.
🔨:hammer:Add or update development scripts.
🌐:globe-with-meridians:Internationalization and localization.
✏️:pencil2:Fix typos.
💩:poop:Write bad code that needs to be improved.
⏪️:rewind:Revert changes.
🔀:twisted-rightwards-arrows:Merge branches.
📦️:package:Add or update compiled files or packages.
👽️:alien:Update code due to external API changes.
🚚:truck:"Move or rename resources (e.g.: files, paths, routes)."
📄:page-facing-up:Add or update license.
💥:boom:Introduce breaking changes.
🍱:bento:Add or update assets.
♿️:wheelchair:Improve accessibility.
💡:bulb:Add or update comments in source code.
🍻:beers:Write code drunkenly.
💬:speech-balloon:Add or update text and literals.
🗃️:card-file-box:Perform database related changes.
🔊:loud-sound:Add or update logs.
🔇:mute:Remove logs.
👥:busts-in-silhouette:Add or update contributor(s).
🚸:children-crossing:Improve user experience / usability.
🏗️:building-construction:Make architectural changes.
📱:iphone:Work on responsive design.
🤡:clown-face:Mock things.
🥚:egg:Add or update an easter egg.
🙈:see-no-evil:Add or update a .gitignore file.
📸:camera-flash:Add or update snapshots.
⚗️:alembic:Perform experiments.
🔍️:mag:Improve SEO.
🏷️:label:Add or update types.
🌱:seedling:Add or update seed files.
🚩:triangular-flag-on-post:Add, update, or remove feature flags.
🥅:goal-net:Catch errors.
💫:dizzy:Add or update animations and transitions.
🗑️:wastebasket:Deprecate code that needs to be cleaned up.
🛂:passport-control:Work on code related to authorization, roles and permissions.
🩹:adhesive-bandage:Simple fix for a non-critical issue.
🧐:monocle-face:Data exploration/inspection.
⚰️:coffin:Remove dead code.
🧪:test-tube:Add a failing test.
👔:necktie:Add or update business logic.
🩺:stethoscope:Add or update healthcheck.
🧱:bricks:Infrastructure related changes.
🧑‍💻:technologist:Improve developer experience.
💸:money-with-wings:Add sponsorships or money related infrastructure.
🧵:thread:Add or update code related to multithreading or concurrency.
🦺:safety-vest:Add or update code related to validation.
```

# Output Format
Please provide only the following
- The commit message (header + body) when you reply.
- Legend of used icons.

# Input Information
Please consider this diff and the context when you create the commit message.

## README ####################################################################
```
{readme_content}
```
<end of README>

## git ls-files (without tests) ##############################################
```
{git_ls_files}
```

## git diff ##################################################################
```
{git_diff}
```

## Previous message ##########################################################
This might be correct or misleading
```
{message}
```

## Optional description ######################################################
This is important notes about this commit
```
{description}
```
