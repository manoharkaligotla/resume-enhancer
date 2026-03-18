async function enhance() {
  const resume = document.getElementById("resume").value;
  const role = document.getElementById("role").value;

  const res = await fetch("/api/enhance", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ resume, role })
  });

  const data = await res.json();

  document.getElementById("output").innerHTML = `
    <h3>Summary</h3>
    <p>${data.summary}</p>
    <h3>Keywords</h3>
    <p>${data.keywords.join(", ")}</p>
    <h3>Missing</h3>
    <p>${data.missing.join(", ")}</p>
  `;
}
