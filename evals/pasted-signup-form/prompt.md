---
tags: [code-review-team]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Task]
---

review this signup form code from my site before i ship it. it sends the signup to the shop's api. save the report to report.md

```js
async function signUp(event) {
  event.preventDefault();
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const age = parseInt(document.getElementById('age').value);
  console.log('signing up', email, password);
  if (age < 18) { alert('You must be 18 or older'); return; }
  const resp = await fetch('https://api.myshop.com/users?token=a8f3k2j9x7', {
    method: 'POST',
    body: JSON.stringify({ name, email, password, age, admin: false })
  });
  const data = await resp.json();
  document.getElementById('msg').innerHTML = 'Welcome, ' + name + '!';
}
document.getElementById('form').addEventListener('submit', signUp);
```
