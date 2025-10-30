document.getElementById('review-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const language = document.getElementById('language').value;
  const code = document.getElementById('code').value;
  const resultBox = document.getElementById('result-box');
  const reviewText = document.getElementById('review-text');
  const score = document.getElementById('score');

  if (!language || !code.trim()) {
    alert('Please select a language and enter your code.');
    return;
  }

  try {
    //await clearOldReview();
    // Show loading text immediately
    reviewText.textContent = "Analyzing your code... please wait.";
    resultBox.classList.remove('hidden');
    score.textContent = "";

    // Send the request to backend
    const response = await fetch('http://127.0.0.1:5000/api/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language, code })
    });

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Review API Response:", data);

    // Ensure we got proper data
    if (!data.review_text) {
      reviewText.textContent = "No feedback received from server.";
      return;
    }

    // ✅ Show review results first
    reviewText.innerHTML = marked.parse(data.review_text);
    score.textContent = `Code Quality Score: ${data.score}/10`;
    resultBox.classList.remove('hidden');
    resultBox.scrollIntoView({ behavior: 'smooth' });

  //   After displaying review result:
    // setTimeout(() => {
    //   loadHistory();
    // }, 5000); // wait 5 seconds before loading history

   loadHistory();

    // Save the latest review to localStorage
    // await saveLastReview(data);


  } catch (error) {
    console.error("Error connecting to backend:", error);
    alert("There was an error connecting to the backend. Check if Flask is running.");
  }
});

async function loadHistory() {
  const response = await fetch("http://127.0.0.1:5000/api/reviews");
  const data = await response.json();

  const historyContainer = document.getElementById("history");
  historyContainer.innerHTML = "";

  if (!Array.isArray(data) || data.length === 0) {
    historyContainer.innerHTML = "<p>No previous reviews found.</p>";
    return;
  }

  // group by language
  const grouped = {};
  data.forEach(review => {
    if (!grouped[review.language]) grouped[review.language] = [];
    grouped[review.language].push(review);
  });

  for (const [language, reviews] of Object.entries(grouped)) {
    const langSection = document.createElement("details");
    langSection.classList.add("language-section");

    const langSummary = document.createElement("summary");
    langSummary.textContent = `${language} (${reviews.length} reviews)`;
    langSection.appendChild(langSummary);

    // add each review
    reviews.forEach(review => {
      const details = document.createElement("details");
      details.classList.add("history-item");

      const summary = document.createElement("summary");
      summary.textContent = `Review #${review.id} | Score: ${review.score}/10 | ${new Date(review.created_at).toLocaleString()}`;

      const content = document.createElement("div");
      content.classList.add("review-content");
      content.innerHTML = `
        <pre><code>${review.code}</code></pre>
        <div class="review-text">${marked.parse(review.review_text)}</div>
      `;

      // Delete button
      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.classList.add("delete-btn");
      deleteBtn.addEventListener("click", async (ev) => {
        ev.stopPropagation(); // prevent toggling the details element
        if (!confirm(`Delete Review #${review.id}? This cannot be undone.`)) return;

        try {
          const delResp = await fetch(`http://127.0.0.1:5000/api/review/${review.id}`, {
            method: "DELETE"
          });

          if (delResp.ok) {
            // refresh history after successful delete
            await loadHistory();
          } else {
            const err = await delResp.json().catch(() => ({}));
            alert("Delete failed: " + (err.error || delResp.statusText));
          }
        } catch (error) {
          console.error("Delete error:", error);
          alert("Network error deleting review.");
        }
      });

      // append in order: summary -> (content + delete)
      details.appendChild(summary);
      // place delete button in the content area (or anywhere you prefer)
      content.appendChild(deleteBtn);
      details.appendChild(content);
      langSection.appendChild(details);
    });

    historyContainer.appendChild(langSection);
  }
}


// document.getElementById("load-history-btn").addEventListener("click", () => {
//   loadHistory();
//   document.getElementById("history-section").scrollIntoView({ behavior: "smooth" });
// });


// === 🧠 Restore last review on reload ===
// document.addEventListener("DOMContentLoaded", () => {
//   const lastReview = localStorage.getItem("lastReview");
//   if (lastReview) {
//     const data = JSON.parse(lastReview);
//     const resultBox = document.getElementById("result-box");
//     const reviewText = document.getElementById("review-text");
//     const score = document.getElementById("score");

//     reviewText.innerHTML = marked.parse(data.review_text);
//     score.textContent = ` Code Quality Score: ${data.score}/10`;
//     resultBox.classList.remove("hidden");
//   }
// });

// === 🧹 Clean start on page load (do NOT restore previous review) ===
document.addEventListener("DOMContentLoaded", () => {
  // Remove any previously saved review from localStorage
  localStorage.removeItem("lastReview");

  // Hide the review result box for a fresh page
  const resultBox = document.getElementById("result-box");
  const reviewText = document.getElementById("review-text");
  const score = document.getElementById("score");

  reviewText.textContent = ""; // clear text
  score.textContent = "";      // clear score
  resultBox.classList.add("hidden");
});

// });
// // === 🧹 Hide any saved review on page load (do not restore) ===
// document.addEventListener("DOMContentLoaded", () => {
//   localStorage.removeItem("lastReview"); // Clear any previous review
//   const resultBox = document.getElementById("result-box");
//   resultBox.classList.add("hidden"); // Keep the review box hidden by default
// });


// // === 💾 Save latest review after receiving it ===
async function saveLastReview(data) {
  localStorage.setItem("lastReview", JSON.stringify(data));
}


// ✅ Collapse review box when loading history
document.getElementById("load-history-btn").addEventListener("click", () => {
const resultBox = document.getElementById("result-box");
resultBox.classList.add("hidden"); // collapse review display
loadHistory();
document.getElementById("history-section").scrollIntoView({ behavior: "smooth" });
});



