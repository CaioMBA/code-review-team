const POSTS = [
  { title: "Moving my blog off WordPress", href: "posts/wordpress.html", date: "2026-09-14" },
  { title: "Notes on SQLite in production", href: "posts/sqlite.html", date: "2026-08-02" },
  { title: "A tiny static site generator", href: "posts/ssg.html", date: "2026-06-21" },
];

function renderPosts() {
  const list = document.getElementById("posts");
  for (const post of POSTS) {
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = post.href;
    link.textContent = post.title;
    const date = document.createElement("time");
    date.dateTime = post.date;
    date.textContent = post.date;
    item.append(link, " ", date);
    list.append(item);
  }
}

renderPosts();
