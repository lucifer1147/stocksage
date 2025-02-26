<script>
  import ParameterInputComponent from "/src/components/parameteInputForm/parameterInputComponent.svelte";

  let optimizerOptions = ["adamw", "adam", "rmsprop"];
  let schedulerOptions = ["steplr", "cosineannealinglr", "reduceonplateau"];

  const paramPresets = {
    sm: {
      numLayers: 5,
      hiddenSize: 512,
      learningRate: 0.001,
      batchSize: 16,
      dropoutProb: 0.2,
      addFeatures: [],
      timeFrame: 20,
      saveExtrasToFile: true,
      saveModelAs: "cu_stock_model",
      checkpointsIter: 20,
      maxEpochs: 50,
      minEpochs: 10,
      patience: 10,
      plotLoss: true,
      optimizerChoice: "adamw",
      schedulerChoice: "steplr",
    },
    md: {
      numLayers: 6,
      hiddenSize: 1024,
      learningRate: 0.0005,
      batchSize: 16,
      dropoutProb: 0.2,
      addFeatures: [],
      timeFrame: 20,
      saveExtrasToFile: true,
      saveModelAs: "md_stock_model",
      checkpointsIter: 20,
      maxEpochs: 50,
      minEpochs: 10,
      patience: 10,
      plotLoss: true,
      optimizerChoice: "adamw",
      schedulerChoice: "steplr",
    },
    lg: {
      numLayers: 8,
      hiddenSize: 2048,
      learningRate: 0.0001,
      batchSize: 16,
      dropoutProb: 0.2,
      addFeatures: [],
      timeFrame: 20,
      saveExtrasToFile: true,
      saveModelAs: "lg_stock_model",
      checkpointsIter: 20,
      maxEpochs: 50,
      minEpochs: 10,
      patience: 10,
      plotLoss: true,
      optimizerChoice: "adamw",
      schedulerChoice: "steplr",
    }, 
    xl: {
      numLayers: 10,
      hiddenSize: 4096,
      learningRate: 0.00005,
      batchSize: 16,
      dropoutProb: 0.2,
      addFeatures: [],
      timeFrame: 20,
      saveExtrasToFile: true,
      saveModelAs: "xl_stock_model",
      checkpointsIter: 20,
      maxEpochs: 50,
      minEpochs: 10,
      patience: 10,
      plotLoss: true,
      optimizerChoice: "adamw",
      schedulerChoice: "steplr",  
    },
    cu: {}
  }

  let preset = $state('cu')
  let trainingParams = $state({
    tickers: {
      value: ["NVDA", "AAPL", "MSFT", "AMZN"],
      name: "Tickers",
      desc: "List of stock tickers to train the model on.",
    },
    numLayers: {
      value: 5,
      name: "Number of Layers",
      desc: "Number of layers in the neural network.",
    },
    hiddenSize: {
      value: 512,
      name: "Hidden Layer Size",
      desc: "Number of units per hidden layer.",
    },
    learningRate: {
      value: 0.001,
      name: "Learning Rate",
      desc: "Step size for the optimizer to update weights.",
    },
    batchSize: {
      value: 16,
      name: "Batch Size",
      desc: "Number of samples processed before updating the model.",
    },
    dropoutProb: {
      value: 0.2,
      name: "Dropout Probability",
      desc: "Fraction of neurons to drop during training to prevent overfitting.",
    },
    addFeatures: {
      value: [],
      name: "Additional Features",
      desc: "Extra features to include in training (e.g., volume, indicators).",
    },
    timeFrame: {
      value: 20,
      name: "Time Frame",
      desc: "Number of past days used as input for predictions.",
    },
    saveExtrasToFile: {
      value: true,
      name: "Save Extras",
      desc: "Whether to save additional training details to a file.",
    },
    saveModelAs: {
      value: "sm_stock_model",
      name: "Model Save Name",
      desc: "Filename for saving the trained model.",
    },
    checkpointsIter: {
      value: 20,
      name: "Checkpoint Interval",
      desc: "Save model checkpoint every N iterations.",
    },
    maxEpochs: {
      value: 50,
      name: "Maximum Epochs",
      desc: "Max number of training epochs before stopping.",
    },
    minEpochs: {
      value: 10,
      name: "Minimum Epochs",
      desc: "Minimum epochs to train before early stopping.",
    },
    patience: {
      value: 10,
      name: "Patience",
      desc: "Number of epochs to wait without improvement before stopping.",
    },
    plotLoss: {
      value: true,
      name: "Plot Loss Curve",
      desc: "Whether to plot loss during training.",
    },
    optimizerChoice: {
      value: "adamw",
      name: "Learning Rate Optimizer",
      desc: "Optimizer used for training (adam, adamw, sgd, etc.).",
    },
    schedulerChoice: {
      value: "steplr",
      name: "Learning Rate Scheduler",
      desc: "Scheduler type for adjusting learning rate over time.",
    },
    debug: {
      value: false,
      name: "Debug Mode",
      desc: "Enable debug mode for additional logs and insights.",
    },
    verbose: {
      value: false,
      name: "Verbose Logging",
      desc: "Enable detailed logs during training.",
    },
    logToFile: {
      value: false,
      name: "Log to File",
      desc: "Write training logs to a file for later analysis.",
    },
    forceCompleteEpochs: {
      value: false,
      name: "Force Complete Epochs",
      desc: "Ensure training completes full epochs even if early stopping is triggered.",
    },
  });

  let formStep = $state(0);
  let stepHistory = [];

  let activeComponent = $state('')

  $inspect(activeComponent)
</script>

<div class="w-full h-full bg-neutral-900 flex items-center justify-center">
  <div class="w-[90%] h-[80%] bg-white rounded-2xl flex">
    <div class="w-[60%] h-full rounded-l-2xl flex flex-wrap text-black">
      <h1
        class="w-full h-[5%] text-3xl flex items-center justify-center py-10 font-bold"
      >
        Specify Training Parameters
      </h1>

      <div class="w-full h-[5%] flex px-7 gap-x-1">
        {#each [0, 1, 2, 3, 4, 5] as step}
          <button
            class={"w-full h-full transition-all " +
              (formStep > step
                ? " bg-blue-600 text-blue-600"
                : formStep === step
                  ? " bg-indigo-700 text-indigo-700"
                  : " bg-gray-200 text-gray-200") +
              (step === 0 ? " rounded-l-full" : "") +
              (step === 5 ? " rounded-r-full" : "")}

            onclick={() => {
              stepHistory.push(formStep);
              formStep = step;
            }}>.</button
          >
        {/each}
      </div>

      <ParameterInputComponent
        bind:trainingParams
        bind:formStep
        bind:preset
        bind:activeComponent

        {schedulerOptions}
        {optimizerOptions}
        {paramPresets}
      />

      <div class="flex justify-between w-full h-[15%] px-10 pb-6">
        <button
          class={"bg-blue-600 rounded-lg text-center w-1/6 text-xl font-bold text-white disabled:bg-blue-300 hover:bg-blue-700 transition-all"}
          onclick={() => {
            formStep = stepHistory.pop();
          }}
          disabled={stepHistory.length === 0 ? true : false}>Back</button
        >
        <button
          class={"bg-blue-600 rounded-lg text-center w-1/6 text-xl font-bold text-white disabled:bg-blue-300 hover:bg-blue-700 transition-all"}
          onclick={() => {
            stepHistory.push(formStep);
            if ((formStep === 1) && (preset !== 'cu')) formStep = 4
            else formStep = formStep + 1;
          }}
          disabled={formStep === 6 ? true : false}>Next</button
        >
      </div>
    </div>

    <div class="w-[40%] h-full rounded-r-2xl bg-gray-300"></div>
  </div>
</div>
