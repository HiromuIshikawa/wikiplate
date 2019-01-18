<template>
  <div class="sidebar">
    <router-link class= "sidebar-item" tag="div" :to="{ name: 'Template'}" exact>記事テンプレート</router-link>
    <router-link class= "sidebar-item" tag="div" :to="{ name: 'Similars'}">類似記事</router-link>
    <router-link class= "sidebar-item" tag="div" :to="{ name: 'About'}">About Wikiplate</router-link>
  </div>
</template>

<script>
export default {
  name: 'SideBar'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .sidebar-item {
    background-color: gray;
    padding-left: 12%;
    padding-top: 2%;
    padding-bottom: 2%;
    font-size: 20px;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .sidebar-item:hover {
    background-color: rgb(91, 91, 91);
  }

  .router-link-active {
    background-color: rgb(91,91,91);
  }
</style>
