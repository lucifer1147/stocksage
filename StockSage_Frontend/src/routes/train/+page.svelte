<script>
  import ParameterInputComponent from "/src/components/parameteInputForm/parameterInputComponent.svelte";

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

  let formStep = $state(0);
  let stepHistory = [];
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
        {schedulerOptions}
        {optimizerOptions}
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
            formStep = formStep + 1;
          }}
          disabled={formStep === 6 ? true : false}>Next</button
        >
      </div>
    </div>

    <div class="w-[40%] h-full rounded-r-2xl bg-gray-300"></div>
  </div>
</div>
