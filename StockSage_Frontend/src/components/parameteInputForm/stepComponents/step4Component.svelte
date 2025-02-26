<script>
    import InputComponent from "../specificComponents/inputComponent.svelte";
    
    let { trainingParams = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
    <InputComponent
      width="w-1/4"
      title={trainingParams.maxEpochs.name}
      bind:binder={trainingParams.maxEpochs.value}
      inputType="number"
      placeholder="50"
    />
    <InputComponent
      width="w-1/4"
      title={trainingParams.minEpochs.name}
      bind:binder={trainingParams.minEpochs.value}
      inputType="number"
      placeholder="10"
    />
    <InputComponent
      width="w-1/4"
      title={trainingParams.batchSize.name}
      bind:binder={trainingParams.batchSize.value}
      inputType="number"
      placeholder="16"
    />
    <InputComponent
      width="w-1/4"
      title={trainingParams.patience.name}
      bind:binder={trainingParams.patience.value}
      inputType="number"
      placeholder="10"
    />

    <InputComponent
      width="w-1/3"
      title={trainingParams.checkpointsIter.name}
      bind:binder={trainingParams.checkpointsIter.value}
      inputType="number"
      placeholder="20"
    />
</div>
