<script>
  import SwitchComponent from "../specificComponents/switchComponent.svelte";

  let { trainingParams = $bindable(), activeComponent = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10 pl-20">
  <SwitchComponent
    title={trainingParams.saveExtrasToFile.name}
    bind:binder={trainingParams.saveExtrasToFile.value}
    bind:activeComponent
    width="w-full"
  />
  <SwitchComponent
    title={trainingParams.plotLoss.name}
    bind:binder={trainingParams.plotLoss.value}
    bind:activeComponent
    width="w-full"
  />
  <SwitchComponent
    title={trainingParams.debug.name}
    bind:binder={trainingParams.debug.value}
    bind:activeComponent
    width="w-full"
  />
  <SwitchComponent
    title={trainingParams.logToFile.name}
    bind:binder={trainingParams.logToFile.value}
    bind:activeComponent
    width="w-full"
  />
  <SwitchComponent
    title={trainingParams.forceCompleteEpochs.name}
    bind:binder={trainingParams.forceCompleteEpochs.value}
    bind:activeComponent
    width="w-full"
  />
  <SwitchComponent
    title={trainingParams.verbose.name}
    bind:binder={trainingParams.verbose.value}
    bind:activeComponent
    width="w-full"
  />
</div>
