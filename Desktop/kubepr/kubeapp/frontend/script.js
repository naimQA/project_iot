const API = "http://localhost:3000/etudiants";

// Charger les étudiants existants
async function load() {
  const r = await fetch(API);
  const d = await r.json();
  const tBody = document.getElementById("t");
  tBody.innerHTML = d.map(
    s => `<tr>
            <td>${s.id}</td>
            <td>${s.nom}</td>
            <td>${s.prenom}</td>
            <td>${s.email}</td>
            <td>${s.age}</td>
          </tr>`
  ).join('');
}

// Envoyer le formulaire en POST
document.getElementById("f").addEventListener("submit", async (e) => {
  e.preventDefault(); // empêche le reload de la page

  const nom = document.getElementById("nom").value;
  const prenom = document.getElementById("prenom").value;
  const email = document.getElementById("email").value;
  const age = parseInt(document.getElementById("age").value);

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nom, prenom, email, age })
  });

  const data = await res.json();
  console.log(data); // voir la réponse
  load(); // recharge le tableau
  e.target.reset(); // vide le formulaire
});

load();
