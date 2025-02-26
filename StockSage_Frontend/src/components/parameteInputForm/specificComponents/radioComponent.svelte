<script>
  let {
    width,
    title,
    options,
    selected = $bindable(),
    activeComponent = $bindable(),
  } = $props();
</script>

<div class="w-full h-full flex flex-wrap">
  {#each options as { value, name }}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="w-full h-1/6 flex text-lg items-center p-3"
      onmouseenter={() => {
        activeComponent = name;
      }}
      onmouseleave={() =>{
        activeComponent = "";
      }}
    >
      <input
        type="radio"
        class="p-2"
        id={`id-${value}`}
        bind:group={selected}
        {value}
      />

      <label for={`id-${value}`} class="w-1/2 mx-3">{name}</label>
    </div>
  {/each}
</div>
