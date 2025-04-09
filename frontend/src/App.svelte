<script>
    import { Router, Route } from "svelte-routing";
    import MainPage from "./MainPage.svelte";
    import ErrPage from "./ErrPage.svelte";
    import Login from "./Login.svelte";

    export let url = "";
</script>

<Router {url}>
    <Route path="/"><Login /></Route>
    <Route path="/main" component={MainPage}></Route>
    <Route path="/err" component={ErrPage}></Route>
</Router>
