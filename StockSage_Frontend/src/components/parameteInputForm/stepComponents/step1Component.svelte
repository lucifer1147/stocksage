<script>
  import InputComponent from "../specificComponents/inputComponent.svelte";

  let { trainingParams = $bindable() } = $props();
</script>

<div class="w-full h-[60%] flex flex-wrap p-10">
  <InputComponent
    width="w-full"
    title={trainingParams.saveModelAs.name}
    bind:binder={trainingParams.saveModelAs.value}
    inputType="text"
    placeholder="sm_stock_model"
  />
  <InputComponent
    width="w-full"
    title={trainingParams.tickers.name}
    bind:binder={trainingParams.tickers.value}
    inputType="text"
    placeholder="NVDA, AAPL, MSFT, AMZN"
  />
  <InputComponent
    width="w-full"
    title={trainingParams.addFeatures.name}
    bind:binder={trainingParams.addFeatures.value}
    inputType="text"
    placeholder="RSI, MACD"
  />
</div>
