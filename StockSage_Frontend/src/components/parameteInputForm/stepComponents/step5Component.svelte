<script>
    import SelectComponent from "../specificComponents/selectComponent.svelte";

    let { trainingParams = $bindable(), optimizerOptions, schedulerOptions, activeComponent = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
    <SelectComponent
      title={trainingParams.optimizerChoice.name}
      options={optimizerOptions}
      bind:selected={trainingParams.optimizerChoice.value}
      bind:activeComponent
      width="w-full h-24"
    />
    <SelectComponent
      title={trainingParams.schedulerChoice.name}
      options={schedulerOptions}
      bind:selected={trainingParams.schedulerChoice.value}
      bind:activeComponent
      width="w-full h-24"
    />
</div>