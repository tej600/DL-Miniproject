async function upload() {
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image");
    return;
  }

  let formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("https://YOUR_BACKEND_URL/process", {
      method: "POST",
      body: formData
    });

    const blob = await response.blob();
    document.getElementById("output").src = URL.createObjectURL(blob);

  } catch (error) {
    console.error(error);
    alert("Error processing image");
  }
}