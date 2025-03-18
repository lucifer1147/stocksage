/** @type {import('./$types').PageLoad} */
import { trainingParamsStore } from '$lib/store';

export const ssr = false;

export async function load({}) {
    let data;
    trainingParamsStore.subscribe((val)=>{
        data = val;
    })
    return {data};
}