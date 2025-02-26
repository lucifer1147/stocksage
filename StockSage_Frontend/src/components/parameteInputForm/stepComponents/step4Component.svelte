<script>
    import InputComponent from "../specificComponents/inputComponent.svelte";
    
    let { trainingParams = $bindable(), activeComponent = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
    <InputComponent
      width="w-1/2"
      title={trainingParams.maxEpochs.name}
      bind:binder={trainingParams.maxEpochs.value}
      bind:activeComponent
      inputType="number"
      placeholder="50"
    />
    <InputComponent
      width="w-1/2"
      title={trainingParams.minEpochs.name}
      bind:binder={trainingParams.minEpochs.value}
      bind:activeComponent
      inputType="number"
      placeholder="10"
    />
    <InputComponent
      width="w-1/2"
      title={trainingParams.batchSize.name}
      bind:binder={trainingParams.batchSize.value}
      bind:activeComponent
      inputType="number"
      placeholder="16"
    />
    <InputComponent
      width="w-1/2"
      title={trainingParams.patience.name}
      bind:binder={trainingParams.patience.value}
      bind:activeComponent
      inputType="number"
      placeholder="10"
    />

    <InputComponent
      width="w-full"
      title={trainingParams.checkpointsIter.name}
      bind:binder={trainingParams.checkpointsIter.value}
      bind:activeComponent
      inputType="number"
      placeholder="20"
    />
</div>
