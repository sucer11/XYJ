<script>
    import { onMount } from "svelte";
    import { currentMail } from "./stores.ts";

    $: mail = $currentMail;
    export let onBack;

    let question = "";
    let answer = "";
    let isLoading = false; // 新增状态变量，用于控制加载动画的显示


    async function askQuestion() {
        isLoading = true;
        const response = await fetch(
            `http://localhost:13271/ask?uid=${$currentMail.uid}&question=${encodeURIComponent(question)}`,
        );
        isLoading = false;
        if (response.ok) {
            const data = await response.text();
            // 将答案按换行符分割成数组
            answer = data.split('\n').map(line => line.trim()).filter(line => line.length > 0);;
            
            console.log("Fetched answer:", answer);
        } else {
            answer = ["Failed to get an answer. Please try again."];
            console.log($currentMail)
        }
    }

    onMount(() => {
        console.log("mail", mail);
    });
</script>

<div class="mail-view">
    <button on:click={onBack} class="back-button">返回</button>
    <h1 class="mail-subject">{mail.email.Subject}</h1>
    <p><strong>发件人: </strong>{mail.email.From}</p>
    <p><strong>日期: </strong>{mail.email.Date}</p>

    <div class="mail-summary">
        <h2 class="summary-header">概要</h2>
        <p>{mail.summary}</p>
    </div>

    <div class="mail-category">
        <h2 class="category-header">分类</h2>
        <p>{mail.category}</p>
    </div>

    <div class="mail-content">
        <h2 class="content-header">原文</h2>
        <p>{#if mail.email.Content}
            {console.log('邮件原文:', mail.email.Content)}
            {mail.email.Content}
        {/if}</p>
    </div>

    <!-- 添加提问功能 -->
    <div class="ask-question">
        <input
            type="text"
            placeholder="输入你的问题"
            bind:value={question}
            class="question-input"
        />
        <button on:click={askQuestion} class="ask-button">提问</button>
        <!-- 添加加载动画 -->
        <div class="loading-spinner" aria-busy={isLoading}></div>
    </div>

    {#if answer}
        <div class="answer">
            <h2 class="answer-header">答案</h2>
            <div class="answer-content">
                {#each answer as line}
                    <p>{line}</p>
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .loading-spinner {
        border: 4px solid #f3f3f3; /* Light grey */
        border-top: 4px solid #3498db; /* Blue */
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 2s linear infinite;
        display: none; /* 默认不显示 */
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* 当 isLoading 为 true 时显示加载动画 */
    .loading-spinner[aria-busy="true"] {
        display: block;
    }

    .ask-question {
        margin-top: 16px;
    }

    .question-input {
        width: 100%;
        padding: 8px 16px;
        margin-bottom: 8px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }

    .ask-button {
        background-color: #ff758c;
        font-size: 16px;
        color: #fff;
        border: none;
        padding: 8px 16px;
        cursor: pointer;
        border-radius: 8px;
    }

    .answer {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 16px;
        margin-top: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .answer-header {
        font-size: 20px;
        margin: 16px 0;
        color: #333;
    }

    .answer-content {
        white-space: pre-line; /* 保留换行符 */
        font-size: 16px;
        color: #333;
        margin: 8px 0;
        line-height: 1.6;
    }

    .mail-view {
        background: linear-gradient(45deg, #6dd5fa, #ff758c);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        color: #333;
    }

    .back-button {
        background-color: #6dd5fa;
        font-size: 16px;
        color: #333;
        margin: 8px 0;

        border: none;
        padding: 8px 16px;
        cursor: pointer;
        margin-bottom: 16px;
        border-radius: 8px;
    }

    .mail-subject {
        font-size: 24px;
        margin: 16px 0;
        color: #fff;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }

    .summary-header,
    .category-header {
        font-size: 20px;
        margin: 16px 0;
        /* color: #fff; */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }

    .mail-summary,
    .mail-category,
    .mail-content {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .mail-summary p,
    .mail-category p,
    .mail-content p {
        font-size: 16px;
        color: #333;
        margin: 8px 0;
    }
</style>
