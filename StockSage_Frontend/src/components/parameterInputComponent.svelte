<script>
    import InputComponent from "./inputComponent.svelte";
    import SelectComponent from "./selectComponent.svelte";
    import SwitchComponent from "./switchComponent.svelte";

    let {trainingParams = $bindable(), optimizerOptions, schedulerOptions} = $props();
</script>

<div class="w-full h-[80%] flex flex-wrap p-5">
    <InputComponent
      width="w-full"
      title="Save Model As"
      bind:binder={trainingParams.saveModelAs}
      inputType="text"
      placeholder="sm_stock_model"
    />
    <InputComponent
      width="w-1/2"
      title="Tickers"
      bind:binder={trainingParams.tickers}
      inputType="text"
      placeholder="NVDA, AAPL, MSFT, AMZN"
    />
    <InputComponent
      width="w-1/2"
      title="Additional Features"
      bind:binder={trainingParams.addFeatures}
      inputType="text"
      placeholder="RSI, MACD"
    />

    <InputComponent
      width="w-1/4"
      title="Maximum Epochs"
      bind:binder={trainingParams.maxEpochs}
      inputType="number"
      placeholder="50"
    />
    <InputComponent
      width="w-1/4"
      title="Minimum Epochs"
      bind:binder={trainingParams.minEpochs}
      inputType="number"
      placeholder="10"
    />
    <InputComponent
      width="w-1/4"
      title="Batch Size"
      bind:binder={trainingParams.batchSize}
      inputType="number"
      placeholder="16"
    />
    <InputComponent
      width="w-1/4"
      title="Patience"
      bind:binder={trainingParams.patience}
      inputType="number"
      placeholder="10"
    />

    <InputComponent
      width="w-1/3"
      title="Number of Layers"
      bind:binder={trainingParams.numLayers}
      inputType="number"
      placeholder="5"
    />
    <InputComponent
      width="w-1/3"
      title="Size of Hidden Layers"
      bind:binder={trainingParams.hiddenSize}
      inputType="number"
      placeholder="512"
    />
    <InputComponent
      width="w-1/3"
      title="Learning Rate"
      bind:binder={trainingParams.learningRate}
      inputType="number"
      placeholder="512"
    />
    
    <InputComponent
      width="w-1/3"
      title="Dropout Probability"
      bind:binder={trainingParams.dropoutProb}
      inputType="number"
      placeholder="0.2"
    />
    <InputComponent
      width="w-1/3"
      title="TimeFrame"
      bind:binder={trainingParams.timeFrame}
      inputType="number"
      placeholder="20"
    />

    <InputComponent
      width="w-1/3"
      title="Iteration for Checkpoints"
      bind:binder={trainingParams.checkpointsIter}
      inputType="number"
      placeholder="20"
    />

    <SelectComponent
      title="Optimizer Choice"
      options={optimizerOptions}
      bind:selected={trainingParams.optimizerChoice}
      width="w-1/2"
    />
    <SelectComponent
      title="Scheduler Choice"
      options={schedulerOptions}
      bind:selected={trainingParams.schedulerChoice}
      width="w-1/2"
    />

    <SwitchComponent
      title="Save Extras to File"
      bind:binder={trainingParams.saveExtrasToFile}
      width="w-1/6"
    />
    <SwitchComponent
      title="Plot the loss Graph"
      bind:binder={trainingParams.plotLoss}
      width="w-1/6"
    />
    <SwitchComponent
      title="Debug Mode"
      bind:binder={trainingParams.debug}
      width="w-1/6"
    />
    <SwitchComponent
      title="Log To File"
      bind:binder={trainingParams.logToFile}
      width="w-1/6"
    />
    <SwitchComponent
      title="Force Complete Epochs"
      bind:binder={trainingParams.forceCompleteEpochs}
      width="w-1/6"
    />
    <SwitchComponent
      title="Verbose Mode"
      bind:binder={trainingParams.verbose}
      width="w-1/6"
    />

</div>