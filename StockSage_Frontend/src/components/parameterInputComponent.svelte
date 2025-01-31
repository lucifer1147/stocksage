<script>
    import InputComponent from "./inputComponent.svelte";
    import SelectComponent from "./selectComponent.svelte";
    import SwitchComponent from "./switchComponent.svelte";

    let {trainingParams = $bindable(), optimizerOptions, schedulerOptions} = $props();
</script>

<div class="w-full h-[80%] flex flex-wrap p-5">
    <InputComponent
      width="w-full"
      title={trainingParams.saveModelAs.name}
      bind:binder={trainingParams.saveModelAs.value}
      inputType="text"
      placeholder="sm_stock_model"
    />
    <InputComponent
      width="w-1/2"
      title={trainingParams.tickers.name}
      bind:binder={trainingParams.tickers.value}
      inputType="text"
      placeholder="NVDA, AAPL, MSFT, AMZN"
    />
    <InputComponent
      width="w-1/2"
      title={trainingParams.addFeatures.name}
      bind:binder={trainingParams.addFeatures.value}
      inputType="text"
      placeholder="RSI, MACD"
    />

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

    <InputComponent
      width="w-1/3"
      title={trainingParams.checkpointsIter.name}
      bind:binder={trainingParams.checkpointsIter.value}
      inputType="number"
      placeholder="20"
    />

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