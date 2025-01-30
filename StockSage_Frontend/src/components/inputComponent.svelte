<script>
  let { width, inputType, placeholder, binder = $bindable(), title } = $props();
  console.log(width, binder)
</script>

<div
  class={`flex ${width} h-[10%] rounded-xl text-black text-lg font-semibold font-mono`}
>
  <p class="bg-gray-500 rounded-l-xl w-full flex items-center justify-center">
    {title}
  </p>
  <input
    type={inputType}
    class="bg-gray-200 outline-none border-none rounded-r-xl w-full"
    {placeholder}
    bind:value={binder}
  />
</div>
