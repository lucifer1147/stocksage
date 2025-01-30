<script>
	import '../app.css';
	let { children } = $props();
</script>

<div class="h-full w-full">
	<nav class="w-full h-[10%] bg-blue-900">

	</nav>
	<div class="w-full h-[90%]">
		{@render children()}
	</div>
</div>
