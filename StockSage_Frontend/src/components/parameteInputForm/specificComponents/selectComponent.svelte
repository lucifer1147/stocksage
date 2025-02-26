<script>
  let {
    width,
    title,
    options,
    selected = $bindable(),
    activeComponent = $bindable(),
  } = $props();
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class={`${width} h-16 rounded-xl text-black text-lg font-semibold font-mono flex p-1`}
  onmouseenter={() => {activeComponent = title}}
  onmouseleave={() => {activeComponent = ""}}
>
  <label
    for={`${title}_id`}
    class="w-1/3 flex items-center justify-center text-center bg-gray-300 border-2 border-gray-400 border-r-0 rounded-l-xl p-2 h-full"
    >{title}</label
  >
  <select
    id={`${title}_id`}
    bind:value={selected}
    class="bg-gray-100 border-2 border-gray-400 text-gray-900 text-sm rounded-r-lg focus:ring-blue-500 focus:border-blue-500 block w-2/3 p-2.5"
  >
    {#each options as value}
      <option {value}>{value}</option>
    {/each}
  </select>
</div>
