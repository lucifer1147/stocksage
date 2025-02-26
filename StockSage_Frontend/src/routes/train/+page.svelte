<script>
  import ParameterInputComponent from "/src/components/parameteInputForm/parameterInputComponent.svelte";
  import {
    trainingParamsNonReactive,
    paramPresets,
    optionToParameter,
  } from "./data";

  let optimizerOptions = ["adamw", "adam", "rmsprop"];
  let schedulerOptions = ["steplr", "cosineannealinglr", "reduceonplateau"];
  let stepHistory = [];

  let trainingParams = $state({ ...trainingParamsNonReactive });
  let preset = $state("cu");
  let formStep = $state(0);
  let activeComponent = $state("");

  let activeOption = $derived(optionToParameter[activeComponent]);

  $inspect(activeOption);
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
            if (formStep === 1 && preset !== "cu") formStep = 4;
            else formStep = formStep + 1;
          }}
          disabled={formStep === 6 ? true : false}>Next</button
        >
      </div>
    </div>

    <div class="w-[40%] h-full rounded-r-2xl bg-gray-300">
      <div class="w-full h-[80%]">
        <h2
          class="w-full h-[5%] text-3xl flex items-center justify-center py-10 font-bold"
        >
          Training Parameter Description
        </h2>
        <ul class="w-full h-[95%] p-5 list-disc">
          <li class="flex">
            <div class="w-1/3">Option Name</div> - &nbsp;
            <div class="w-2/3">{activeComponent}</div>
          </li>
          <li class="flex">
            <div class="w-1/3">Backend Option Name</div> - &nbsp;
            <div class="w-2/3">{activeOption}</div>
          </li>
          <li class="flex">
            <div class="w-1/3">Description</div> - &nbsp;
            <div class="w-2/3">{trainingParams[activeOption].desc}</div>
          </li>
        </ul>
      </div>

      <div class="w-full h-[20%] px-10 pb-8 pt-6">
        <button
          class="bg-blue-600 rounded-lg text-center w-full text-xl font-bold text-white hover:bg-blue-700 transition-all h-full disabled:bg-blue-300"
          disabled={formStep !== 6 ? true : false}>Begin Training</button
        >
      </div>
    </div>
  </div>
</div>
