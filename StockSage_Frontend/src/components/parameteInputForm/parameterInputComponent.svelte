<script>
  import Step1Component from "./stepComponents/step1Component.svelte";
  import Step2Component from "./stepComponents/step2Component.svelte";
  import Step3Component from "./stepComponents/step3Component.svelte";
  import Step4Component from "./stepComponents/step4Component.svelte";
  import Step5Component from "./stepComponents/step5Component.svelte";
  import Step6Component from "./stepComponents/step6Component.svelte";

  import ReviewComponent from "./reviewComponent.svelte";

  let {
    trainingParams = $bindable(),
    formStep = $bindable(),
    optimizerOptions,
    schedulerOptions,
  } = $props();
</script>

<div class="display: contents">
  {#if formStep === 0}
    <Step1Component bind:trainingParams />
  {:else if formStep === 1}
    <Step2Component />
  {:else if formStep === 2}
    <Step3Component bind:trainingParams />
  {:else if formStep === 3}
    <Step4Component bind:trainingParams />
  {:else if formStep === 4}
    <Step5Component bind:trainingParams {optimizerOptions} {schedulerOptions} />
  {:else if formStep === 5}
    <Step6Component bind:trainingParams />
  {:else if formStep === 6}
    <ReviewComponent bind:trainingParams />
  {/if}
</div>
