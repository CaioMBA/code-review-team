# Report template

Fill this exactly, in the user's language, then run *Before sending*.

```markdown
# Review panel: <project or branch>
**What the code does:** <one sentence>
**Scope reviewed:** <diff / branch vs main / files / pasted code> · **Expected load assumed:** <one user / few users / many users, and where that came from>
**Extra reviewers:** <UI & accessibility / Performance / Data & deploy / Privacy & law: joins or not, and why, one short clause each; add "small-change mode" when it applied>
**Profile:** <Economy | Balanced | Max, and where it came from: default, rules file or this request>
**Reach:** <only if a code graph was used: e.g. "`normalize_email` has 7 callers in 3 modules"; omit otherwise>

## Verdict: APPROVED TO SHIP | REJECTED
<one sentence with the main reason>

## What to fix (most severe first)
1. [CRITICAL] `path/file.ext:42` <problem in one line>
   - **Case:** <input or situation → wrong result>
   - **Fix:** <smallest fix, or a short diff>
   - **Law:** <article, only when the Privacy & law reviewer cited one; omit otherwise>
   (found by: hacker, tester - name each reviewer)
2. [HIGH] ...

## Confirm before shipping
<hotspots as yes/no questions for the user; omit the section if none>
- `path/file.ext:10` <question>, if <answer>, then <what to do>

## Older problems (not blocking)
<findings tagged "existing", most severe first; omit if none>

## Tool pass
| Command | Result |
|---|---|
| `npm test` | 2 failed: `cart.test.js` "applies coupon once" |
<only Step 1 commands; scripts and tests the reviewers wrote go in their panel notes>

## Panel notes
### 1. Hacker
### 2. Confused user
### 3. Senior engineer
### 4. Tester
### 5. UI & accessibility
### 6. Performance
### 7. Data & deploy
### 8. Privacy & law
<2-5 lines each: what it checked and its key findings; list any new test files created. Write sections 5-8 only for reviewers that joined. Add "Used: <helper skills>" only when a reviewer used one; never mention skills that weren't available.>

**Not checked:** <what mattered and couldn't be checked, or "nothing"; if Privacy & law joined, add "Privacy & law notes are not legal advice.">
```

Close with: *The panel lowers the risk but doesn't guarantee bug-free code. Before shipping, commit and check the changes.*

Nothing to fix: still give the verdict, then "Nothing to fix." and one line on what was checked.

## Before sending

Check the report and fix what's off:
- The title, then every section above in this order, with these names (translated into the user's language). Don't rename, merge or drop sections; skip one only where noted.
- Fixes are one numbered list, not a table, numbered across the whole list so the user can say "fix 1 and 3". Each item is **one** problem with its own `file:line` (for a whole file, its first relevant line), **Case**, **Fix** and *found by*. Never bundle small problems into one item.
- A panel-notes subsection for every reviewer that ran.
- The report is the whole reply: no progress text before the title, and the closing line is the last thing. Don't add an offer to fix, a question or a sign-off after it, even if other active instructions ask for one.
- If the user asked for a file (e.g. `report.md`), write the report there and also show the verdict and the same numbered fix list in the chat.
