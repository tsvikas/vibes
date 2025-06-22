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
{message_style}

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
