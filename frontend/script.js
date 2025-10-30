//event listener added to the form submission
document.getElementById('review-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  //get form values
  const language = document.getElementById('language').value;
  const code = document.getElementById('code').value;
  const resultBox = document.getElementById('result-box');
  const reviewText = document.getElementById('review-text');
  const score = document.getElementById('score');

  if (!language || !code.trim()) { //simple validation to make sureboth feid are filled 
    alert('Please select a language and enter your code.');
    return;
  }

  try { //loading message shown while waiting for backend to respond
    reviewText.textContent = "Analyzing your code... please wait.";
    resultBox.classList.remove('hidden');
    score.textContent = "";

    //requesrt sent to the backend server (Flask API)
    const response = await fetch('http://127.0.0.1:5000/api/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language, code })
    });

    if (!response.ok) { //error thorwn if server fails to respond
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json(); //backend JSON response parsed 
    console.log("✅ Review API Response:", data);

    // ensure backend returns a valid review text
    if (!data.review_text) {
      reviewText.textContent = "No feedback received from server.";
      return;
    }

    reviewText.innerHTML = marked.parse(data.review_text);  //review displayed using markdown parser
    score.textContent = `Code Quality Score: ${data.score}/10`;  //display score calculated
    resultBox.classList.remove('hidden');    //result box made visible
    resultBox.scrollIntoView({ behavior: 'smooth' }); //scoll to the review area, smoothly

   loadHistory(); //load all reviews below, after showing results

  } catch (error) { //backend errors handled
    console.error("Error connecting to backend:", error);
    alert("There was an error connecting to the backend. Check if Flask is running.");
  }
});

//function to laod history of previous code reviews
async function loadHistory() {
  const response = await fetch("http://127.0.0.1:5000/api/reviews"); //backend route to return all reviews called
  const data = await response.json();

  const historyContainer = document.getElementById("history"); //container to show all history
  historyContainer.innerHTML = ""; //any old content cleared

  if (!Array.isArray(data) || data.length === 0) { //shows a simple message, if noe reviews yet
    historyContainer.innerHTML = "<p>No previous reviews found.</p>";
    return;
  }

  //group by the reviews by programming language
  const grouped = {};
  data.forEach(review => {
    if (!grouped[review.language]) grouped[review.language] = [];
    grouped[review.language].push(review);
  });

  //sections created for each language
  for (const [language, reviews] of Object.entries(grouped)) {
    const langSection = document.createElement("details"); //collapsible section created 
    langSection.classList.add("language-section");

    const langSummary = document.createElement("summary"); //summary
    langSummary.textContent = `${language} (${reviews.length} reviews)`;
    langSection.appendChild(langSummary);

    reviews.forEach(review => { //HTML elements created for each review
      const details = document.createElement("details");
      details.classList.add("history-item");

      const summary = document.createElement("summary"); //summary for each review 
      summary.textContent = `Review #${review.id} | Score: ${review.score}/10 | ${new Date(review.created_at).toLocaleString()}`;

      const content = document.createElement("div"); //actual contecnt inside 
      content.classList.add("review-content");
      content.innerHTML = `
        <pre><code>${review.code}</code></pre>
        <div class="review-text">${marked.parse(review.review_text)}</div>
      `;

      const deleteBtn = document.createElement("button"); //delete button created for each review 
      deleteBtn.textContent = "Delete";
      deleteBtn.classList.add("delete-btn");

      //delete button functionality
      deleteBtn.addEventListener("click", async (ev) => {
        ev.stopPropagation(); //prevent toggling the details element
        if (!confirm(`Delete Review #${review.id}? This cannot be undone.`)) return;

        try {
          const delResp = await fetch(`http://127.0.0.1:5000/api/review/${review.id}`, {
            method: "DELETE"
          });

          if (delResp.ok) { //reload the list if deletion is successful 
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

      details.appendChild(summary); //append summary to details
      content.appendChild(deleteBtn);
      details.appendChild(content);
      langSection.appendChild(details);
    });

    historyContainer.appendChild(langSection); //finished section added to the page
  }
}

//page restes when first loaded
document.addEventListener("DOMContentLoaded", () => {
  localStorage.removeItem("lastReview"); //old local data cleared

  const resultBox = document.getElementById("result-box"); //main elements
  const reviewText = document.getElementById("review-text");
  const score = document.getElementById("score");

  reviewText.textContent = ""; //clear text
  score.textContent = "";      //clear score
  resultBox.classList.add("hidden"); //hidden until code is reviewd
});

//review box collapses when clicked on load history button
document.getElementById("load-history-btn").addEventListener("click", () => {
const resultBox = document.getElementById("result-box");
resultBox.classList.add("hidden"); // collapse review display
loadHistory(); //review history refreshed
document.getElementById("history-section").scrollIntoView({ behavior: "smooth" });
});