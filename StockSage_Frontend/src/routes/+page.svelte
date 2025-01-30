<script>
  import { goto } from "$app/navigation";
</script>

<div class="bg-neutral-900 h-full w-full">
  <h1 class="text-5xl flex justify-center text-white font-normal w-full pt-10">
    Welcome to &nbsp; <p class="text-blue-500 font-bold">StockSage</p>
  </h1>
  <h2 class="text-2xl flex justify-center text-white font-light w-full py-3">
    AI-Powered Stock Predictions, Just for You
  </h2>

  <div
    class="flex my-10 p-10 w-[90%] mx-auto bg-neutral-800 h-[50%] rounded-2xl justify-around items-center"
  >
    <div
      class="h-full text-white border-r-2 my-2 border-x-black w-full flex flex-wrap justify-center hover:bg-neutral-700 p-4 rounded-l-xl transition-all"
    >
      <h3
        class="font-semibold text-2xl pb-3 text-wrap flex w-full justify-center text-center"
      >
        Train Your Custom Model
      </h3>
      <p class="text-white text-lg font-light text-center">
        Tailor a prediction model to match your unique strategies. Train it with
        the data that matters most to you.
      </p>
    </div>
    <div
      class="h-full text-white border-x-2 my-2 border-x-black w-full flex flex-wrap justify-center hover:bg-neutral-700 p-4 transition-all"
    >
      <h3
        class="font-semibold text-2xl pb-3 text-wrap flex w-full justify-center text-center"
      >
        Predict the Stocks You Want
      </h3>
      <p class="text-white text-lg font-light text-center">
        Use advanced AI to forecast stock prices and trends, helping you stay
        ahead of the curve.
      </p>
    </div>
    <div
      class="h-full text-white border-x-2 my-2 border-x-black w-full flex flex-wrap justify-center hover:bg-neutral-700 p-4 transition-all"
    >
      <h3
        class="font-semibold text-2xl pb-3 text-wrap flex w-full justify-center text-center"
      >
        Track Your Portfolio
      </h3>
      <p class="text-white text-lg font-light text-center">
        Keep an eye on your investments and watch your portfolio grow with
        real-time tracking.
      </p>
    </div>
    <div
      class="h-full text-white border-x-2 my-2 border-x-black w-full flex flex-wrap justify-center hover:bg-neutral-700 p-4 transition-all"
    >
      <h3
        class="font-semibold text-2xl pb-3 text-wrap flex w-full justify-center text-center"
      >
        AI Integration
      </h3>
      <p class="text-white text-lg font-light text-center">
        Harness the power of AI to give you insights that go beyond traditional
        analysis.
      </p>
    </div>
    <div
      class="h-full text-white border-l-2 my-2 border-x-black w-full flex flex-wrap justify-center hover:bg-neutral-700 p-4 rounded-r-xl transition-all"
    >
      <h3
        class="font-semibold text-2xl pb-3 text-wrap flex w-full justify-center text-center"
      >
        User Friendly GUI
      </h3>
      <p class="text-white text-lg font-light text-center">
        No complicated setups or confusing interfaces. Stocksage is designed to
        be intuitive and easy to navigate for anyone.
      </p>
    </div>
  </div>

  <div
    class="my-10 h-[10%] bg-blue-700 w-[90%] mx-auto rounded-2xl flex justify-center"
  >
    <button
      class="w-full h-full hover:bg-blue-600 text-white text-2xl font-extrabold rounded-l-2xl transition-all"
      on:click={() => goto("/predict")}>Predict Stocks</button
    >
    <button
      class="w-full h-full hover:bg-blue-600 text-white text-2xl font-extrabold border-x-4 border-white transition-all"
      on:click={() => goto("/train")}>Train Your Model</button
    >
    <button
      class="w-full h-full hover:bg-blue-600 text-white text-2xl font-extrabold rounded-r-2xl transition-all"
      on:click={() => goto("/view")}>View Stocks</button
    >
    <!-- <button>Track Portfolio</button> -->
  </div>
</div>
