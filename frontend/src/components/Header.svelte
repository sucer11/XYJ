<script>
  import {mailCount, selectedCategory} from "./stores.ts";
  import { onMount } from 'svelte'; // 确保导入 onMount
  export let categories = [];
  // export let onCategoryChange; // 添加这个导出属性
  // 默认选项为空字符串，表示显示所有邮件
  let localSelectedCategory = "";
  onMount(async () => {
        try {
            const response = await fetch("http://localhost:13271/get_categories");
            categories = await response.json();
            console.log("Fetched categories raw data:", categories);

            // 将对象的键作为分类列表
            categories = Array.isArray(categories) ? rawData : Object.keys(categories);

            // 打印处理后的 categories 到控制台
            console.log("Processed categories array:", categories);

        } catch (error) {
            console.error("获取分类失败:", error);
        }

        // return () => clearInterval(interval);
    });

    function handleCategoryChange(category) {
        console.log("Selected category:", category);
        selectedCategory.set(category);
    }
</script>

<header class="header">
  <div class="mail-count">{$mailCount} 封邮件</div>
  <!-- <div class="verification-code" in:fade out:fade>{verificationCode}</div> -->
   <!-- 添加选择器 -->
  <select bind:value={localSelectedCategory} name="categorySelect" id="categorySelect" on:change={(e) => handleCategoryChange(e.target.value)}>
    <option value="">全部邮件</option>
    {#each categories as category}
      <option value={category}>{category}</option>
    {/each}
  </select>
</header>

<style>
  .header {
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    font-size: 24px;
    font-weight: bold;
    background: linear-gradient(45deg, #6DD5FA, #FF758C);
    color: white;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
    position: relative;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  }

  

  .header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(45deg, #6DD5FA, #FF758C);
    opacity: 0.7;
    border-radius: 0 0 12px 12px;
  }

  .mail-count {
    background: rgba(255, 255, 255, 0.2);
    padding: 12px 24px;
    border-radius: 24px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  .mail-count:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }

  select {
    background: rgba(181, 73, 179, 0.203);
    padding: 10px 20px;
    border-radius: 12px;
    color: rgb(255, 255, 255);
    border: none;
    font-size: 18px;
    transition: box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  select:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
</style>
