<script>
  let { trainingParams = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <p class="text-lg py-2">Start training with the following parameters:</p>
  <div class="w-full h-[90%] overflow-auto px-8 bg-gray-200 rounded-xl">
    <ul class="list-disc">
      {#each Object.entries(trainingParams) as [key, value]}
        <li class="w-full flex">
          <div class="w-1/2 font-semibold">{value.name}</div>
          <div class="w-1/2">{value.value}</div>
        </li>
      {/each}
    </ul>
  </div>
</div>
