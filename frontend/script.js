// Replace simulation with API call
const formData = new FormData();
formData.append("image", file);

fetch("http://127.0.0.1:5000/upload", {
  method: "POST",
  body: formData
})
.then(response => response.blob())
.then(data => {
  const url = URL.createObjectURL(data);
  document.getElementById('outputImg').src = url;
  document.getElementById('downloadBtn').style.display = "inline-block";
});
