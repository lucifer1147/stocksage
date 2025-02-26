<script>
  let {
    width,
    inputType,
    placeholder,
    binder = $bindable(),
    activeComponent = $bindable(),
    title,
  } = $props();
</script>

<!-- svelte-ignore a11y_interactive_supports_focus -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class={`flex ${width} h-20 rounded-xl text-black text-lg font-semibold font-mono p-1`}
  onmouseenter={() => {
    activeComponent = title;
  }}
  onmouseleave={() => {
    activeComponent = "";
  }}
>
  <label
    for={`${title}_id`}
    class="bg-gray-300 border-2 border-gray-400 border-r-0 rounded-l-xl w-full flex items-center justify-center text-center p-2"
  >
    {title}
  </label>
  <input
    type={inputType}
    id={`${title}_id`}
    class="bg-gray-200 border-2 border-gray-400 focus:outline-none rounded-r-xl w-full pl-10"
    {placeholder}
    bind:value={binder}
  />
</div>
