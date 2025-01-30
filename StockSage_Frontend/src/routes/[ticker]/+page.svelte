<script>
    /** @type {import('./$types').PageProps} */
    import { onMount } from "svelte";
    import "chartjs-adapter-luxon";
    import {
        Chart,
        TimeScale,
        LinearScale,
        BarController,
        BarElement,
    } from "chart.js";
    import zoomPlugin from "chartjs-plugin-zoom";
    // import "chartjs-adapter-date-fns";
    // import {de} from 'date-fns/locale'

    let { data } = $props();
    let chart;
    const candlestickData = data.data;

    let start_date = candlestickData[0].x
    let end_date = candlestickData[candlestickData.length - 1].x

    let range_min = candlestickData[candlestickData.length - 101].x
    let range_max = candlestickData[candlestickData.length - 1].x

    range_max.setDate(range_max.getDate() + 5)

    // for (let i; i < candlestickData.length; i++) {
    //     console.log(i)
    // }

    Chart.register(
        zoomPlugin,
        TimeScale,
        LinearScale,
        BarController,
        BarElement,
    );

    onMount(() => {
        const ctx = document
            .getElementById("candlestick-chart")
            .getContext("2d");

        // Transform data for High-Low lines and Open-Close bars
        const highLowData = candlestickData.map((d) => ({
            x: d.x,
            y: [d.l, d.h],
        }));

        const openCloseData = candlestickData.map((d) => ({
            x: d.x,
            y: d.o > d.c ? [d.c, d.o] : [d.o, d.c],
        }));

        const openCloseColors = candlestickData.map((d) =>
            d.o > d.c ? "rgba(255, 0, 0, 1)" : "rgba(0, 255, 0, 1)",
        );

        const highLowColors = candlestickData.map((d) =>
            d.o > d.c ? "rgba(255, 0, 0, 0.5)" : "rgba(0, 255, 0, 0.5)",
        );

        // Initialize Chart.js
        chart = new Chart(ctx, {
            type: "bar", // Use a bar chart
            data: {
                datasets: [
                    {
                        label: "High-Low",
                        type: "bar", // Draw High-Low as lines
                        data: highLowData,
                        backgroundColor: highLowColors,
                        parsing: {
                            yAxisKey: "y", // Parse y values directly
                        },
                        categoryPercentage: 0.05,
                    },
                    {
                        label: "Open-Close",
                        type: "bar", // Draw Open-Close as bars
                        data: openCloseData,
                        backgroundColor: openCloseColors,
                        parsing: {
                            yAxisKey: "y", // Parse y values directly
                        },
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: "x", // Allow panning on both axes
                            rangeMin: {
                                x: range_min,
                            },
                            rangeMax: {
                                x: range_max
                            }
                        },
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true,
                            },
                            mode: "x",
                            rangeMin: {
                                x: range_min,
                            },
                            rangeMax: {
                                x: range_max
                            }
                        },
                    },
                    tooltip: {
                        enabled: true, // Enable tooltips
                        callbacks: {
                            // Customize the tooltip label
                            label: (tooltipItem) => {
                                const { o, h, l, c } = tooltipItem.raw;
                                const date = tooltipItem.label;
                                return `Date: ${date}\nOpen: ${o}\nHigh: ${h}\nLow: ${l}\nClose: ${c}`;
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        type: "time",
                        stacked: true,
                        time: {
                            min: start_date.toDateString(),
                            max: end_date.toDateString(),
                            unit: "day",
                            stepSize: "1",
                        },
                        title: {
                            display: true,
                            text: "Date",
                        },
                    },
                    y: {
                        type: "linear",
                        title: {
                            display: true,
                            text: "Price",
                        },
                    },
                },
            },
        });
        
        // chart.zoom({x:1.9})
        // chart.update()
        // console.log(0)

        return () => chart.destroy(); // Clean up on unmount
    });
</script>

<div class="h-full w-full bg-neutral-900 p-10 flex flex-col">
    <div
        class="w-full text-white text-3xl flex items-center justify-center h-20 font-black"
    >
        {data.ticker}
    </div>
    <canvas id="candlestick-chart" class=""></canvas>
</div>
