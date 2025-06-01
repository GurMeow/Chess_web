async function set_depth() {
  const formData = new FormData();
  const res = Number(document.getElementById("depth_input").value);
  formData.append("depth", res / 2);
  document.getElementById("depth_display").innerText = `Depth (${res})`;
  await fetch("http://127.0.0.1:5000/set_depth", {
    method: "POST",
    body: formData,
  });
}
