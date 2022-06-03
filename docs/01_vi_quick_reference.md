# Vim Quick Reference

## Modes

There are four (4) modes in the vim/vi editor:

- Normal
- Insert
- Visual
- Replace

### Normal

The vim/vi editor is in *normal*  mode upon entering. Editing is not allowed in this mode. 
The alpha-numeric keys act as navigation keys for moving around the document.

- h - moves one position to the left (same as &larr;)
- j - moves one position down (same as &darr;)
- k - moves one position up (same as &uarr;)
- l - moves one position to the right (same as &rarr;)

There are times when moving a single character at a time is not fast enough. In these cases,
you can use *motion* keys

- w - word: Words are delineated by spaces; however, special characters are also recognized as separate words. The *w* motion key takes you to the beginning (first character) of the next word.
- e - end: The delimiter characters include the space and special characters, but the cursor is placed at the last character 
of the current word.
- W - word: Special characters are not recognized as delimiters; otherwise, similar to *w* motion key.
- E - end: Special characters are not recognized as delimiters; othwerwise, similar to *e* motion key.
- b - back: Takes the cursor back to the previous location.
- $ - end of line: Places the cursor at the end of the current line.
- 0 - beginning of line: Places the cursor at the beginning of the current line.

### Insert

Editing is performed in the *insert* mode.

### Visual

You select text via the keyboard without the need for using an external device such as a mouse.

### Replace

In this mode, you are able to find and replace text.

## Navigation

## Editing

## Save/Exit

## References

[[1] Vim Crash Course | How to edit files quickly in CKAD/CKA exam, https://www.youtube.com/watch?v=knyJt8d6C_8](https://www.youtube.com/watch?v=knyJt8d6C_8)