<script>
  import RadioComponent from "../specificComponents/radioComponent.svelte";

  let {
    trainingParams = $bindable(),
    preset = $bindable(),
    paramPresets,
    activeComponent = $bindable(),
  } = $props();

  let options = [
    {
      value: "cu",
      name: "Custom",
    },
    {
      value: "sm",
      name: "Small",
    },
    {
      value: "md",
      name: "Medium",
    },
    {
      value: "lg",
      name: "Large",
    },
    {
      value: "xl",
      name: "Extra Large",
    },
  ];
  $effect(() => {
    const newParams = {}; // Create a completely new object

    for (const [key, value] of Object.entries(trainingParams)) {
      newParams[key] = { ...value }; // Deep copy the nested object
      if (key in paramPresets[preset]) {
        newParams[key].value = paramPresets[preset][key]; // Update safely
      }
    }

    if (JSON.stringify(newParams) !== JSON.stringify(trainingParams)) {
      trainingParams = newParams; // Assign the new object to trigger reactivity
    }
  });
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <RadioComponent {options} bind:selected={preset} width="w-1/6" bind:activeComponent />
</div>
