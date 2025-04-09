<script>
    export let status = 404;
    export let message = "Page not found";
</script>

<style>
    .error-page {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
        color: #333;
    }

    .error-code {
        font-size: 6rem;
        font-weight: bold;
    }

    .error-message {
        font-size: 1.5rem;
    }
</style>

<div class="error-page">
    <div class="error-code">{status}</div>
    <div class="error-message">{message}</div>
</div>