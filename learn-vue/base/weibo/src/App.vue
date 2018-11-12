<template>
    <div id="app">
        <Top></Top>
        <router-view/>
    </div>
</template>

<script>

    import Top from "./components/Top";

    export default {
        name: "App",
        components: {Top},
    }
</script>
<style>
    * {
        margin: 0;
        padding: 0;
    }

    a {
        text-decoration: none;
        color: black;
    }

    li {
        list-style: none;
    }
</style>