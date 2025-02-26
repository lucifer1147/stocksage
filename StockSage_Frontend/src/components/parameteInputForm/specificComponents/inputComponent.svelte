<script>
  let { width, inputType, placeholder, binder = $bindable(), title } = $props();
</script>

<div
  class={`flex ${width} h-16 rounded-xl text-black text-lg font-semibold font-mono p-1`}
>
  <label for={`${title}_id`} class="bg-gray-300 border-2 border-gray-400 border-r-0 rounded-l-xl w-full flex items-center justify-center text-center p-2">
    {title}
  </label>
  <input
    type={inputType}
    id = {`${title}_id`}
    class="bg-gray-200 border-2 border-gray-400 focus:outline-none rounded-r-xl w-full pl-10"
    {placeholder}
    bind:value={binder}
  />
</div>
