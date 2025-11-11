document.getElementById('rewriteBtn').addEventListener('click', async () => {
  const email = document.getElementById('emailInput').value.trim();
  const tone = document.getElementById('tone').value;
  const output = document.getElementById('outputText');

  if (!email) {
    output.value = "Please enter an email first.";
    return;
  }

  output.value = "Rewriting...";

  try {
    const response = await fetch("/api/rewrite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, tone }),
    });

    const data = await response.json();
    if (data.rewritten_email) {
      output.value = data.rewritten_email;
    } else {
      output.value = "Error: " + (data.error || "Unknown error occurred.");
    }
  } catch (error) {
    output.value = "Network error: " + error.message;
  }
});

document.getElementById('copyBtn').addEventListener('click', () => {
  const text = document.getElementById('outputText').value;
  if (!text) {
    alert("Nothing to copy!");
    return;
  }
  navigator.clipboard.writeText(text);
  alert("Copied to clipboard!");
});