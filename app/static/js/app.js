const predictBtn = document.getElementById("predictBtn");
const inputText = document.getElementById("inputText");
const resultDiv = document.getElementById("result");
const loadingDiv = document.getElementById("loading");

predictBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) {
    resultDiv.textContent = "Please enter some text.";
    resultDiv.classList.remove("hidden");
    return;
  }

  // Show loading and hide result
  loadingDiv.classList.remove("hidden");
  resultDiv.classList.add("hidden");

  try {
    // Step 1: Initiate the prediction call
    const initialResponse = await fetch(
      "https://titanicc73-fake-news-model.hf.space/gradio_api/call/predict",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: [text],
        }),
      },
    );

    if (!initialResponse.ok) {
      throw new Error("Failed to initiate prediction");
    }

    const initialData = await initialResponse.json();
    const eventId = initialData?.event_id;

    if (!eventId) {
      throw new Error("Failed to retrieve Event ID");
    }

    // Step 2: Polling for results
    let predictionComplete = false;
    let retries = 10; // Max number of retries
    let trueProbability = 0;
    let fakeProbability = 0;

    while (!predictionComplete && retries > 0) {
      const predictionResponse = await fetch(
        `https://titanicc73-fake-news-model.hf.space/gradio_api/call/predict/${eventId}`,
      );

      if (!predictionResponse.ok) {
        throw new Error("Failed to fetch prediction result");
      }

      const rawText = await predictionResponse.text();
      console.log("Raw Response:", rawText);

      // Parse the raw event-stream-like response
      const eventMatch = rawText.match(/event:\s+complete/);
      const dataMatch = rawText.match(/data:\s+(.+)/);

      if (eventMatch && dataMatch) {
        const rawData = dataMatch[1].trim();

        try {
          const parsedData = JSON.parse(rawData);
          console.log("Parsed Data:", parsedData);

          // Extract true and fake probabilities
          trueProbability = parsedData?.[0]?.[0]?.[0] || 0;
          fakeProbability = parsedData?.[0]?.[0]?.[1] || 0;

          predictionComplete = true;
        } catch (jsonError) {
          throw new Error("Failed to parse prediction data");
        }
      } else {
        // Wait before polling again
        await new Promise((resolve) => setTimeout(resolve, 1000));
        retries--;
      }
    }

    if (predictionComplete) {
      let resultMessage = "";
      if (trueProbability > fakeProbability) {
        resultMessage = `📰 The news is likely **TRUE** (${(trueProbability * 100).toFixed(2)}%)`;
        resultDiv.className = "text-green-500 mt-2";
      } else {
        resultMessage = `🚨 The news is likely **FAKE** (${(fakeProbability * 100).toFixed(2)}%)`;
        resultDiv.className = "text-red-500 mt-2";
      }

      resultDiv.textContent = resultMessage;
    } else {
      resultDiv.textContent = "Prediction timed out. Please try again.";
      resultDiv.className = "text-gray-500 mt-2";
    }

    resultDiv.classList.remove("hidden");
    loadingDiv.classList.add("hidden");
  } catch (error) {
    console.error("Error:", error.message);
    resultDiv.textContent = "Error: " + error.message;
    resultDiv.className = "text-red-500 mt-2";
    resultDiv.classList.remove("hidden");
    loadingDiv.classList.add("hidden");
  }
});
