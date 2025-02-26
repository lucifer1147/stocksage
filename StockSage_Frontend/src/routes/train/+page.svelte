<script>
  import ParameterInputComponent from "/src/components/parameterInputComponent.svelte";

  let optimizerOptions = ["adamw", "adam", "rmsprop"];
  let schedulerOptions = ["steplr", "cosineannealinglr", "reduceonplateau"];

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

</script>

<div class="w-full h-full bg-neutral-900 flex items-center justify-center">
  <div class="w-[90%] h-[80%] bg-white rounded-2xl flex flex-wrap text-black">
    <h1
      class="w-full h-[20%] text-3xl flex items-center justify-center py-10 font-bold"
    >
      Specify Training Parameters
    </h1>

    <ParameterInputComponent bind:trainingParams={trainingParams} optimizerOptions={optimizerOptions} schedulerOptions={schedulerOptions}/>
  </div>
</div>
