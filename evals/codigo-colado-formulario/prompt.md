---
tags: [code-review-team]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Task]
---

revisa esse codigo do formulario de cadastro do meu site antes de eu subir. ele manda o cadastro pra api da loja. salva o relatorio em relatorio.md

```js
async function cadastrar(event) {
  event.preventDefault();
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;
  const idade = parseInt(document.getElementById('idade').value);
  console.log('cadastrando', email, senha);
  if (idade < 18) { alert('Precisa ter 18 anos'); return; }
  const resp = await fetch('https://api.minhaloja.com/usuarios?token=a8f3k2j9x7', {
    method: 'POST',
    body: JSON.stringify({ nome, email, senha, idade, admin: false })
  });
  const dados = await resp.json();
  document.getElementById('msg').innerHTML = 'Bem-vindo, ' + nome + '!';
}
document.getElementById('form').addEventListener('submit', cadastrar);
```
