<script>
	import Header from "./components/Header.svelte";
	import Footer from "./components/Footer.svelte";
	import MailList from "./components/MailList.svelte";
	import MailView from "./components/MailView.svelte";
	import Settings from "./components/Settings.svelte";

	import { currentMail, selectedCategory } from "./components/stores.ts";
	
	const startPage = "mailList";
	let currentTab = startPage; // 当前显示的标签

	function openMail(mail) {
		currentMail.set(mail);
		currentTab = "mailView";
	}

	function goBack() {
		currentTab = "mailList";
	}

	let categories = [];

	function handleCategoryChange(category) {
		selectedCategory.set(category);
	}

	function handleOpenMail(mail) {
		openMail(mail);
	}
</script>

<div class="layout">
	<Header {categories} />

	<main class="content">
		{#if currentTab === "mailList"}
			<MailList onOpenMail={handleOpenMail} />
		{:else if currentTab === "mailView"}
			<MailView onBack={goBack} />
		{:else if currentTab === "settings"}
			<Settings />
		{/if}
	</main>

	<Footer {currentTab} onTabChange={(tab) => (currentTab = tab)} />
</div>

<style>
	.layout {
		display: flex;
		flex-direction: column;
		height: 100vh; /* 确保布局高度为视窗高度 */
		overflow: hidden;
	}
	/*

	Header,
	Footer {
		position: fixed;
		width: 100%;
		z-index: 1000;
	}

	Header {
		top: 0;
	}

	footer {
		bottom: 0;
	}
	*/
	.content {
		flex: 1;
		overflow-y: auto; /* 允许内容区域滚动 */
		padding: 16px;
		padding-top: 64px; /* 留出顶部标题栏的高度 */
		padding-bottom: 48px; /* 留出底部导航栏的高度 */
		background-color: #f9f9f9;
	}
</style>
