<script>
    import InputComponent from "../specificComponents/inputComponent.svelte";

    let { trainingParams = $bindable(), activeComponent = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <InputComponent
    width="w-1/2"
    title={trainingParams.numLayers.name}
    bind:binder={trainingParams.numLayers.value}
    bind:activeComponent
    inputType="number"
    placeholder="5"
  />
  <InputComponent
    width="w-1/2"
    title={trainingParams.hiddenSize.name}
    bind:binder={trainingParams.hiddenSize.value}
    bind:activeComponent
    inputType="number"
    placeholder="512"
  />
  <InputComponent
    width="w-1/2"
    title={trainingParams.learningRate.name}
    bind:binder={trainingParams.learningRate.value}
    bind:activeComponent
    inputType="number"
    placeholder="512"
  />

  <InputComponent
    width="w-1/2"
    title={trainingParams.dropoutProb.name}
    bind:binder={trainingParams.dropoutProb.value}
    bind:activeComponent
    inputType="number"
    placeholder="0.2"
  />
  <InputComponent
    width="w-full"
    title={trainingParams.timeFrame.name}
    bind:binder={trainingParams.timeFrame.value}
    bind:activeComponent
    inputType="number"
    placeholder="20"
  />
</div>
