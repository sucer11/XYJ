<script>
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";

    let categories = {};
    let newCategory = "";
    let newPrompt = "";
    let expandedCategory = null;
    let rebuildingDatabase = false;

    onMount(async () => {
        try {
            const response = await fetch("http://localhost:13271/get_categories");
            categories = await response.json();
        } catch (error) {
            console.error("获取分类失败:", error);
        }

        // Set up interval to fetch email count
        const interval = setInterval(async () => {
            if (rebuildingDatabase) {
                try {
                    const response = await fetch(
                        "http://localhost:13271/email_count",
                    );
                    emailCount = await response.json();
                } catch (error) {
                    console.error("获取邮件数量失败:", error);
                }
            }
        }, 1000);

        return () => clearInterval(interval);
    });

    async function syncCategoriesWithBackend() {
        try {
            const response = await fetch(
                "http://localhost:13271/set_categories",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(categories),
                },
            );
            if (!response.ok) {
                throw new Error("Failed to sync categories with backend");
            }
        } catch (error) {
            console.error("Error syncing categories:", error);
        }
    }

    function addCategory() {
        if (newCategory && newPrompt) {
            categories = {
                ...categories,
                [newCategory]: newPrompt,
            };
            newCategory = "";
            newPrompt = "";
            syncCategoriesWithBackend(); // Call this after updating categories
        }
    }

    function deleteCategory(category) {
        if (confirm("确定要删除这个分类吗？")) {
            const { [category]: _, ...newCategories } = categories;
            categories = newCategories;
            syncCategoriesWithBackend(); // Call this after updating categories
        }
    }

    function toggleExpand(category) {
        expandedCategory = expandedCategory === category ? null : category;
    }

    async function rebuildDatabase() {
        if (confirm("确定要重建数据库吗？")) {
            rebuildingDatabase = true;
            try {
                let response = await fetch("http://localhost:13271/rebuild_all", {
                    method: "POST",
                });
                if (response.ok) {
                    alert("数据库重建成功！");
                }
            } catch (error) {
                alert("数据库重建失败！");
            } finally {
                rebuildingDatabase = false;
            }
        }
    }
</script>

<div class="settings">
    <h2>现有分类</h2>
    <div class="categories-list">
        {#each Object.entries(categories) as [category, prompt]}
            <div class="category-entry">
                <div class="category-item">
                    <div
                        class="category-header"
                        on:click={() => toggleExpand(category)}
                        on:keypress={() => toggleExpand(category)}
                    >
                        <strong>{category}</strong>

                        <span class="expand-icon"
                            >{expandedCategory === category ? "▼" : "▶"}</span
                        >
                    </div>

                    {#if expandedCategory === category}
                        <div class="category-prompt" transition:fly>
                            {prompt}
                        </div>
                    {/if}
                </div>
                <button
                    class="delete-btn"
                    on:click={() => deleteCategory(category)}>&times;</button
                >
            </div>
        {/each}
    </div>

    <h2>添加新分类</h2>
    <div class="new-category">
        <input type="text" bind:value={newCategory} placeholder="类别名" />
        <textarea bind:value={newPrompt} placeholder="分类 Prompt" rows="3"
        ></textarea>
        <button on:click={addCategory}>添加</button>
    </div>

    <button class="rebuild-button" on:click={rebuildDatabase}>
        重建数据库
    </button>

    {#if rebuildingDatabase}
        <div class="overlay">
            <div class="spinner"></div>
            <p>正在重建数据库...  已处理</p>
        </div>
    {/if}
</div>

<style>
    .settings {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 32px;
        padding: 32px;
        background: linear-gradient(45deg, #6dd5fa, #ff758c);
        border-radius: 24px;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    h2 {
        margin: 0;
        font-size: 2rem;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        font-weight: bold;
    }

    .categories-list {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .category-entry {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        padding: 16px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.5);
    }

    .category-item {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .category-item:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }

    .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px;
        cursor: pointer;
        background: rgba(255, 255, 255, 0.8);
        border-bottom: 2px solid rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }

    .category-header:hover {
        background-color: rgba(255, 255, 255, 0.9);
    }

    .category-header strong {
        font-size: 1.5rem;
        color: #333;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .expand-icon {
        font-size: 1.5rem;
        color: #666;
        transition: transform 0.3s ease;
    }

    .expand-icon:hover {
        transform: rotate(180deg);
    }

    .category-prompt {
        padding: 24px;
        background: rgba(255, 255, 255, 0.8);
        white-space: pre-wrap;
        animation: fly 0.5s ease;
    }

    @keyframes fly {
        0% {
            transform: translateY(20px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }

    .delete-btn {
        width: 40px;
        height: 40px;
        background-color: #ff4d4d;
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .delete-btn:hover {
        background-color: #ff1a1a;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }

    .new-category {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    input,
    textarea {
        width: 100%;
        padding: 16px;
        border: none;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 1rem;
        resize: vertical;
        transition: box-shadow 0.3s ease;
    }

    input:focus,
    textarea:focus {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }

    .rebuild-button {
        margin-top: 16px;
        padding: 16px 32px;
        background-color: #ffcc00;
        color: #333;
        border: none;
        border-radius: 24px;
        font-size: 1.2rem;
        cursor: pointer;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .rebuild-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }

    .rebuild-button:active {
        transform: translateY(0);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }

    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 4px solid #fff;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

</style>
