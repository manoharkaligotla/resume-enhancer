async function enhance() {
  const resume = document.getElementById("resume").value;
  const role = document.getElementById("role").value;

  if (!resume || !role) {
    alert("Please enter resume and role");
    return;
  }

  const res = await fetch("/api/enhance", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ resume, role })
  });

  const data = await res.json();

  if (data.error) {
    document.getElementById("output").innerHTML = `<p style="color:red">${data.error}</p>`;
    return;
  }

  document.getElementById("output").innerHTML = `
    <h3>✨ Summary</h3>
    <p>${data.summary}</p>

    <h3>🔥 Keywords</h3>
    <p>${data.keywords.join(", ")}</p>

    <h3>⚠️ Missing Skills</h3>
    <p>${data.missing.join(", ")}</p>

    <h3>📊 Match Score</h3>
    <p>${data.score}</p>
  `;
}
