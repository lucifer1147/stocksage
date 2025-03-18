<script>
  import { onDestroy, onMount } from "svelte";

  let { data } = $props();
  const params = data.data;

  let ws;
  let messages = $state([]);
  let isTraining = false;

  function connectWebSocket() {
    ws = new WebSocket("ws://localhost:8000/ws/train/");

    ws.onopen = () => {
      console.log("Connected to WebSocket");
      isTraining = true;
    };

    ws.onmessage = (event) => {
      let data = JSON.parse(event.data);
      messages = [...messages, data.message]; // Store received messages
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket Disconnected");
      isTraining = false;
    };
  }

  function startTraining() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      connectWebSocket();
      setTimeout(sendTrainingParams, 500); // Ensure WS is open before sending
    } else {
      sendTrainingParams();
    }
  }

  function sendTrainingParams() {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ params }));
      messages = ["Training started..."];
    }
  }

  function stopTraining() {
    if (ws) {
      ws.close(); // Disconnect WebSocket (triggers stop in backend)
    }
  }

  onDestroy(() => {
    if (ws) {
      ws.close(); // Ensure cleanup on component destroy
    }
  });

  onMount(() => {
    startTraining()
  });
</script>

<div class="h-full w-full bg-neutral-900 flex items-center justify-center">
  <div class="bg-black w-[80%] h-[80%] border-2 border-white rounded-xl p-11 text-white font-mono font-semibold text-lg overflow-auto">
    <ul class="overflow-auto">
      {#each messages as message}
        <li>{message}</li>
      {/each}
    </ul>
  </div>
</div>
