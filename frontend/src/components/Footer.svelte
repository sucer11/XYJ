<script>
  export let currentTab;
  export let onTabChange;
</script>

<footer class="footer">
  <button
    class:active={currentTab === 'mailList'}
    on:click={() => onTabChange('mailList')}
  >
    邮件列表
  </button>
  <button
    class:active={currentTab === 'settings'}
    on:click={() => onTabChange('settings')}
  >
    设置
  </button>
</footer>
<style>
  .footer {
    height: 60px; /* Increased height for a bolder footer */
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: linear-gradient(45deg, #6DD5FA, #FF758C); /* Consistent gradient background */
    color: white;
    box-shadow: 0 -8px 16px rgba(0, 0, 0, 0.3); /* Enhanced shadow for depth */
    position: relative;
    border-radius: 0 0 12px 12px; /* Rounded corners at the bottom */
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out; /* Smooth transition for interactions */
  }

  .footer::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(45deg, #6DD5FA, #FF758C); /* Matching gradient for the top edge */
    opacity: 0.7;
    border-radius: 12px 12px 0 0; /* Matching rounded corners */
  }

  button {
    background: none;
    border: none;
    color: white;
    font-size: 18px; /* Slightly larger font size for better readability */
    cursor: pointer;
    padding: 10px 20px; /* Increased padding for larger touch area */
    border-radius: 10px; /* Slightly larger border radius for softer corners */
    transition: background-color 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), transform 0.3s ease-in-out; /* Smooth transition for interactions */
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3); /* Text shadow for better contrast */
  }

  button:hover {
    background-color: rgba(255, 255, 255, 0.2); /* Slightly more visible hover state */
    transform: scale(1.05); /* Slight scaling on hover */
  }

  button.active {
    background-color: rgba(255, 255, 255, 0.3); /* More visible active state */
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4); /* Enhanced shadow for active state */
  }
</style>
