<script>
  import InputComponent from "/src/components/inputComponent.svelte";

  let trainingParams = $state({
    tickers: ["NVDA", "AAPL", "MSFT", "AMZN"],
    numLayers: 5,
    hiddenSize: 512,
    learningRate: 0.001,
    batchSize: 16,
    dropoutProb: 0.2,
    addFeatures: [],
    timeFrame: 20,
    saveExtrasToFile: true,
    saveModelAs: "sm_stock_model",
    checkpointsIter: 20,
    maxEpochs: 50,
    minEpochs: 10,
    patience: 10,
    plotLoss: true,
  });
</script>

<div class="w-full h-full bg-neutral-900 flex items-center justify-center">
  <div class="w-[90%] h-[80%] bg-white rounded-2xl flex flex-wrap text-black">
    <h1
      class="w-full h-[20%] text-3xl flex items-center justify-center py-10 font-bold"
    >
      Specify Training Parameters
    </h1>

    <div class="w-full h-[80%] flex flex-wrap p-5 gap-5">
      <InputComponent
        width="w-full"
        title="Number of Layers"
        bind:binder={trainingParams.numLayers}
        inputType="number"
        placeholder="5"
      />
      <InputComponent
        width="w-full"
        title="Size of Hidden Layers"
        bind:binder={trainingParams.hiddenSize}
        inputType="number"
        placeholder="512"
      />
      <InputComponent
        width="w-full"
        title="Tickers"
        bind:binder={trainingParams.tickers}
        inputType="text"
        placeholder="NVDA, AAPL, MSFT, AMZN"
      />
    </div>
  </div>
</div>
