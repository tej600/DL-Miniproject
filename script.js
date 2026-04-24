async function upload() {
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];

  let formData = new FormData();
  formData.append("file", file);

  const response = await fetch("https://your-api-url/process", {
    method: "POST",
    body: formData
  });

  const blob = await response.blob();
  document.getElementById("output").src = URL.createObjectURL(blob);
}