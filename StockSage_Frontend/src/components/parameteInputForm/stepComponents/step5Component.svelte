<script>
    import SelectComponent from "../specificComponents/selectComponent.svelte";

    let { trainingParams = $bindable(), optimizerOptions, schedulerOptions } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
    <SelectComponent
      title={trainingParams.optimizerChoice.name}
      options={optimizerOptions}
      bind:selected={trainingParams.optimizerChoice.value}
      width="w-1/2"
    />
    <SelectComponent
      title={trainingParams.schedulerChoice.name}
      options={schedulerOptions}
      bind:selected={trainingParams.schedulerChoice.value}
      width="w-1/2"
    />
</div>