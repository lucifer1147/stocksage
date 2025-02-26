<script>
    import InputComponent from "../specificComponents/inputComponent.svelte";

    let { trainingParams = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <InputComponent
    width="w-1/3"
    title={trainingParams.numLayers.name}
    bind:binder={trainingParams.numLayers.value}
    inputType="number"
    placeholder="5"
  />
  <InputComponent
    width="w-1/3"
    title={trainingParams.hiddenSize.name}
    bind:binder={trainingParams.hiddenSize.value}
    inputType="number"
    placeholder="512"
  />
  <InputComponent
    width="w-1/3"
    title={trainingParams.learningRate.name}
    bind:binder={trainingParams.learningRate.value}
    inputType="number"
    placeholder="512"
  />

  <InputComponent
    width="w-1/3"
    title={trainingParams.dropoutProb.name}
    bind:binder={trainingParams.dropoutProb.value}
    inputType="number"
    placeholder="0.2"
  />
  <InputComponent
    width="w-1/3"
    title={trainingParams.timeFrame.name}
    bind:binder={trainingParams.timeFrame.value}
    inputType="number"
    placeholder="20"
  />
</div>
