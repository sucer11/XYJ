<script lang="ts">
    import { navigate } from "svelte-routing";

    let email = "quoilam@163.com";
    let password = "SXDmuWnphCXGUURV";
    // let email = "18438823698@163.com";
    // let password = "DRjRp6styzY8mFPX";

    function handleSubmit() {
        // Handle login logic here
        fetch(
            `http://localhost:13271/login`,
            { method: "Get", headers: { "Content-Type": "application/json" } },
        )
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Login failed");
                }
            })
            .then((data) => {
                navigate("/main");
            })
            .catch((error) => {
                console.error("Login failed:", error);
            });
    }
</script>
<div class="login-container">
    <h2>Login</h2>
    <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email} required />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                required
            />
        </div>
        <button type="submit">Login</button>
    </form>
</div>

<style>
    .login-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
        max-width: 400px;
        margin: 50px auto;
        padding: 32px;
        background: linear-gradient(45deg, #6DD5FA, #FF758C);
        border-radius: 24px;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease-in-out;
    }

    .login-container:hover {
        transform: translateY(-10px);
    }

    .login-container h2 {
        color: #fff;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .login-container label {
        display: block;
        margin-bottom: 0.5rem;
        color: #fff;
        font-size: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .login-container input {
        width: 100%;
        padding: 16px;
        border: none;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 1rem;
        transition: box-shadow 0.3s ease;
    }

    .login-container input:focus {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }

    .login-container button {
        width: 100%;
        padding: 16px;
        background: linear-gradient(45deg, #6DD5FA, #FF758C);
        color: #fff;
        border: none;
        border-radius: 24px;
        cursor: pointer;
        font-size: 1.2rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .login-container button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }

    .login-container button:active {
        transform: translateY(0);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
