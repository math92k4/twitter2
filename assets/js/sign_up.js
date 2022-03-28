// Sign up form
document.querySelector("#sign_up_form").addEventListener("submit", postUser);

async function postUser(event) {
  event.preventDefault();
  const form = event.target;

  const conn = await fetch("/users", {
    method: "POST",
    body: new FormData(form),
  });

  if (!conn.ok) {
    const error = await conn.json();
    console.log(conn);
    console.log(error);
    return;
  }
  await conn.json();
  window.location.href = "/";
}
