document.querySelector("#sign_in_form").addEventListener("submit", postSession);

async function postSession(event) {
  event.preventDefault();
  const form = event.target;

  const conn = await fetch("/sessions", {
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
