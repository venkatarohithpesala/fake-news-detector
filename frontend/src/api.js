export const analyzeNews = async (text) => {
  try {
    const res = await fetch("http://localhost:5000/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) {
      throw new Error("Failed to fetch");
    }

    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Error during analysis:", err);
    return { error: "API call failed" };
  }
};
