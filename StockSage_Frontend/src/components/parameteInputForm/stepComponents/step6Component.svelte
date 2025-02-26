<script>
  import SwitchComponent from "../specificComponents/switchComponent.svelte";

  let { trainingParams = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <SwitchComponent
    title={trainingParams.saveExtrasToFile.name}
    bind:binder={trainingParams.saveExtrasToFile.value}
    width="w-1/6"
  />
  <SwitchComponent
    title={trainingParams.plotLoss.name}
    bind:binder={trainingParams.plotLoss.value}
    width="w-1/6"
  />
  <SwitchComponent
    title={trainingParams.debug.name}
    bind:binder={trainingParams.debug.value}
    width="w-1/6"
  />
  <SwitchComponent
    title={trainingParams.logToFile.name}
    bind:binder={trainingParams.logToFile.value}
    width="w-1/6"
  />
  <SwitchComponent
    title={trainingParams.forceCompleteEpochs.name}
    bind:binder={trainingParams.forceCompleteEpochs.value}
    width="w-1/6"
  />
  <SwitchComponent
    title={trainingParams.verbose.name}
    bind:binder={trainingParams.verbose.value}
    width="w-1/6"
  />
</div>
