<script>
    import { onMount, onDestroy } from "svelte";
    import { mailCount, selectedCategory } from "./stores.ts";
    import Header from './Header.svelte';

    $: mailCount.update(() => mails.length);

    export let onOpenMail;
    export let onCategoryChange;

    let mails = [];
    let limit = 5;
    let loaded = 0;
    let isLoading = false;

    function handleCategoryChange(category) {
        selectedCategory.update(() => category);
        if (onCategoryChange) {
            onCategoryChange(category);
        }
    }

    // Function to generate a color based on the category
    function getCategoryColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 2) - hash);
        }
        let color = '#';
        for (let i = 0; i < 3; i++) {
            // Lighten each color component
            const value = (hash >> (i * 8)) & 0xFE;
            color += (`00${value.toString(16)}`).substr(-2);
        }
        return color;
    }

    function filterMailsByCategory(mails, category) {
        if (!category) return mails; // 如果没有选择类别，则返回所有邮件
        return mails.filter(mail => mail.category === category);
    }
   
    async function fetchMails() {
        if (isLoading) return;
        isLoading = true;
        fetch(
            `http://localhost:13271/last_email?limit=${limit}&offset=${loaded}`,
        ).then(
            async (response) => {
                const data = await response.json();
                const newMails = data.map((mail) => ({
                    uid: mail[0],
                    email: mail[1],
                    category: mail[2],
                    summary: mail[3],
                }));
                mails = [...mails, ...newMails];
                loaded += newMails.length;
            },
            (error) => {
                console.log("获取邮件失败:", error);
            },
        );
        isLoading = false;
    }

    onMount(async () => {
        await fetchMails();
        window.addEventListener("scroll", handleScroll);
    });

    function handleScroll() {
        if (
            window.innerHeight + window.scrollY >=
            document.body.offsetHeight - 100
        ) {
            if (!isLoading) {
                const spinner = document.createElement("div");
                spinner.className = "loader";
                document.body.appendChild(spinner);
                fetchMails().then(() => {
                    document.body.removeChild(spinner);
                });
            }
        }
    }

    onDestroy(() => {
        window.removeEventListener("scroll", handleScroll);
    });
</script>

<div class="mail-list">
    {#each filterMailsByCategory(mails, $selectedCategory) as mail}
        <div
            class="mail-item"
            on:click={() => onOpenMail(mail)}
            on:keydown={(e) => onOpenMail(mail)}
            role="button"
            tabindex="0"
        >
            <div
                class="mail-category"
                style="background-color: {getCategoryColor(mail.category)}"
            >
                {mail.category}
            </div>
            <div class="mail-title">{mail.email.Subject}</div>
            <div class="mail-sender">{mail.email.From}</div>
            <div class="mail-date">{mail.email.Date}</div>
        </div>
    {/each}
</div>

<style>
    .mail-list {
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 20px;
        /* max-width: 600px; */
        margin: 50px auto;
        background: linear-gradient(45deg, #6dd5fa, #ff758c);
        border-radius: 24px;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        transition:
            transform 0.3s ease-in-out,
            box-shadow 0.3s ease-in-out;
    }

    .mail-item {
        padding: 24px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition:
            transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1),
            box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .mail-item::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        z-index: -1;
        transform: scale(0);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    .mail-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .mail-item:hover::before {
        transform: scale(1);
    }

    .mail-category {
        font-size: 16px;
        color: #333;
        font-weight: bold;
        margin-bottom: 8px;
        padding: 4px 8px;
        border-radius: 8px;
        display: inline-block;
    }

    .mail-title {
        font-weight: 600;
        font-size: 18px;
        color: #333;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
    }

    .mail-sender {
        font-size: 16px;
        color: #666;
        margin-top: 8px;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.3);
    }

    .mail-date {
        font-size: 14px;
        color: #999;
        margin-top: 4px;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.2);
    }
</style>
