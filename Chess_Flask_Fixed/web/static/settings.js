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

async function set_time() {
  const formData = new FormData();
  const time = Number(document.getElementById("timer_input").value);

  formData.append("player_time", time * 60);

  document.getElementById("timer_display").innerText = `Minutes (${time})`;
  await fetch("http://127.0.0.1:5000/change_time", {
    method: "POST",
    body: formData,
  });
}

async function set_timer() {
  const formData = new FormData();
  const timer = document.getElementById("timer_enable_input");

  formData.append("player_timer", timer.checked);

  await fetch("http://127.0.0.1:5000/change_timer", {
    method: "POST",
    body: formData,
  });
}

async function show_all_values()
{
    const request1 = await fetch("http://127.0.0.1:5000/get_depth");
    const response1 = await request1.json()
    console.log(response1);
    document.getElementById("depth_display").innerText = `Depth (${response1 * 2})`;

    const request2 = await fetch("http://127.0.0.1:5000/get_time");
    const response2 = await request2.json()
    console.log(response2);
    console.log(request1);
    document.getElementById("timer_display").innerText = `Minutes (${response2[0] / 60})`;

    document.getElementById("timer_enable_input").checked = response2[1];
}

show_all_values().then();
